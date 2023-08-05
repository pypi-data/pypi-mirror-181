import argparse
import json
import logging
import signal
import traceback
import uuid
from typing import Callable

import grpc
import prometheus_client as prom
import structlog
from google.protobuf.struct_pb2 import Struct, Value
from structlog.types import FilteringBoundLogger

from . import const
from . import kubefox_pb2 as kf
from . import kubefox_pb2_grpc as kf_rpc


class Kit:

    request: kf.Data = None
    response: kf.Data = kf.Data()
    broker: kf_rpc.ComponentServiceStub = None
    log: FilteringBoundLogger = None

    def __init__(self, request: kf.Data, broker: kf_rpc.ComponentServiceStub, log: FilteringBoundLogger) -> None:
        self.request = request
        self.broker = broker
        self.log = log.bind(traceId=request.metadata.span.trace_id)

    def value(self, key: str) -> Value:
        return self.request.values.fields[key]

    def arg(self, key: str) -> Value:
        return self.request.args.fields[key]

    def component(self, name: str):
        return Component(name, self)


class Component:

    _name: str = None
    _kit: Kit = None

    def __init__(self, name: str, kit: Kit) -> None:
        self._name = name
        self._kit = kit

    def invoke(self, args: dict = None, content_type: str = None, content: bytes = None) -> kf.Data:
        args_struct = Struct()
        args_struct.update(args)

        data = kf.Data(
            args=args_struct,
            content_type=content_type,
            content=content,
        )

        return self._kit.broker.InvokeRemoteComponent(
            kf.Request(
                target=self._name,
                parent_id=self._kit.request.metadata.id,
                system_tag=self._kit.request.metadata.system_tag,
                environment=self._kit.request.metadata.environment,
                span=self._kit.request.metadata.span,
                data=data,
            )
        )


class KubeFox:

    entrypoint: Callable = None
    broker: kf_rpc.ComponentServiceStub = None
    sub_id: str = None
    log: FilteringBoundLogger = None

    def entrypoint(self, func: Callable):
        self.entrypoint = func
        return func

    def start(self) -> None:
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

        parser = argparse.ArgumentParser()
        # Adding optional argument
        parser.add_argument(
            "-b",
            "--broker-grpc-addr",
            default="localhost:7070",
            help="address of the broker's gRPC server (default localhost:7070)",
        )
        parser.add_argument(
            "-d",
            "--dev",
            help="Run component in dev mode",
            action=argparse.BooleanOptionalAction,
        )
        args = parser.parse_args()

        if args.dev:
            structlog.configure(
                processors=[
                    structlog.contextvars.merge_contextvars,
                    structlog.processors.add_log_level,
                    structlog.processors.StackInfoRenderer(),
                    structlog.dev.set_exc_info,
                    structlog.dev.ConsoleRenderer(),
                ],
            )
        else:
            structlog.configure(
                processors=[
                    structlog.stdlib.add_log_level,
                    structlog.processors.TimeStamper(key="ts"),
                    structlog.processors.EventRenamer(to="msg"),
                    structlog.processors.JSONRenderer(),
                ]
            )
        self.log = structlog.get_logger("some_logger")

        service_config_json = json.dumps(
            {
                "methodConfig": [
                    {
                        "name": [{}],
                        "retryPolicy": {
                            "maxAttempts": 5,
                            "initialBackoff": "0.25s",
                            "maxBackoff": "2s",
                            "backoffMultiplier": 2,
                            "retryableStatusCodes": ["UNAVAILABLE"],
                        },
                    }
                ]
            }
        )
        options = [
            ("grpc.enable_retries", 1),
            ("grpc.service_config", service_config_json),
        ]

        with grpc.insecure_channel(args.broker_grpc_addr, options=options) as channel:
            self.broker = kf_rpc.ComponentServiceStub(channel)
            try:
                conf = self.broker.GetConfig(kf.ConfigRequest())
                if args.dev:
                    self.log = structlog.get_logger().bind(logger_name=conf.component.name)
                else:
                    self.log = structlog.get_logger().bind(
                        componentId=conf.component.id,
                        componentHash=conf.component.hash,
                        componentName=conf.component.name,
                        componentPart="runtime",
                    )

                self.sub_id = str(uuid.uuid4())
                self.log.info(f"subscribing to broker; addr: {args.broker_grpc_addr}, subscription: {self.sub_id}")

                self._run(self.broker, self.sub_id)

            except BaseException as e:
                self._stop()

    def _run(self, broker: kf_rpc.ComponentServiceStub, sub_id: str) -> None:
        for request in broker.Subscribe(kf.SubscribeRequest(id=sub_id)):
            try:
                kit = Kit(request, broker, self.log)
                if request.metadata.type == const.METRICS_REQUEST_TYPE:
                    self._generate_metrics_response(kit)
                else:
                    self.entrypoint(kit)

                broker.SendResponse(kf.Response(parent_id=request.metadata.id, data=kit.response))

            except Exception as e:
                print(e)
                traceback.print_exc()

    def _stop(self, sig=None, frame=None):
        if self.broker is not None:
            self.log.info(f"unsubscribing from broker; subscription: {self.sub_id}")
            self.broker.Unsubscribe(kf.SubscribeRequest(id=self.sub_id))
        exit()

    def _generate_metrics_response(self, kit: Kit) -> None:
        kit.response.content = prom.generate_latest()
        kit.response.content_type = prom.CONTENT_TYPE_LATEST
        kit.response.metadata.type = const.METRICS_RESPONSE_TYPE
