from __future__ import annotations

import asyncio
import time
from functools import partial
from types import SimpleNamespace
from typing import Type, Generic, Callable, Dict, Any

import loguru
import orjson
from sanic import Sanic, Request
from sanic.response import BaseHTTPResponse

from web_foundation.config import AppConf
from web_foundation.extentions.addons.addon_loader import AddonsLoader
from web_foundation.extentions.error_handler import ExtendedErrorHandler
from web_foundation.extentions.metrics.events import NewMetricEvent
from web_foundation.extentions.metrics.metric import HistogramMetric, CounterMetric, SummaryMetric, Metric
from web_foundation.extentions.realtime.broadcaster import RtBroadcaster
from web_foundation.extentions.realtime.connection import RtEventCallback
from web_foundation.extentions.router import ExtRouter
from web_foundation.extentions.sanic_ext_worker import ExtWorker
from web_foundation.kernel.messaging.channel import IChannel, IMessage, GenericIMessage
from web_foundation.kernel.container import GenericDependencyContainer
from web_foundation.kernel.messaging.dispatcher import IDispatcher, IDispatcherIsolate
from web_foundation.kernel.isolate import Isolate
from web_foundation import settings
from web_foundation.settings_event import SettingsChangeEvent


class App(Generic[GenericDependencyContainer]):
    name: str
    container: GenericDependencyContainer
    sanic: Sanic
    config: AppConf
    dispatcher: IDispatcher
    # listeners: Dict[str, List[AppListener]]
    _rt_listeners = list[tuple[list[Type[IMessage] | str], RtEventCallback, bool]]

    def __init__(self, dependency_container: GenericDependencyContainer,
                 dispatcher: IDispatcher = None):
        self.name = dependency_container.app_config().app_name
        self.container = dependency_container
        self.sanic = Sanic(self.name, loads=orjson.loads, dumps=orjson.dumps,
                           error_handler=ExtendedErrorHandler())

        self.dispatcher = dispatcher if dispatcher else IDispatcher()
        self._rt_listeners = []
        self.add_isolate("Dispatcher", IDispatcherIsolate, dispatcher=self.dispatcher, add_channel=False, daemon=True)

    def add_isolate(self, name: str, isolate_cls: Type[Isolate], daemon=True, add_channel: bool = True, **kwargs):
        """
        Add process to execute with worker manager
        """
        instance = isolate_cls(name, container=self.container, **kwargs)
        if add_channel:
            self.dispatcher.register_isolate(instance)

        def add_nondaemon(s_app: Sanic):
            nonlocal instance

            def override_manage(ident, func, kwargs: Dict[str, Any], transient=False, daemon=True):
                nonlocal s_app
                container = s_app.manager.transient if transient else s_app.manager.durable
                container.append(
                    ExtWorker(ident, func, kwargs, s_app.manager.context, s_app.manager.worker_state, daemon=daemon))

            s_app.manager.manage = override_manage
            s_app.manager.manage(name, instance.run_forked, {}, daemon=daemon)

        if daemon:
            self.sanic.main_process_ready(
                lambda s_app: s_app.manager.manage(name, instance.run_forked, {}))
            # self.sanic.main_process_ready(lambda s_app:s_app.manager.)
        else:
            self.sanic.main_process_ready(lambda s_app: add_nondaemon(s_app))

    def subscribe_worker(self, event_type: list[GenericIMessage | str] | GenericIMessage | str,
                         resolve_callback: RtEventCallback, use_nested_classes: bool = False):
        """
        Subscribe all sanic workers to event[s]
        :param use_nested_classes:
        :param event_type: Name or Class event
        :param resolve_callback: Resolve function
        """
        self._rt_listeners.append((event_type, resolve_callback, use_nested_classes))

    def add_custom_router(self, router: ExtRouter):
        router.ctx.app = self.sanic
        self.sanic.router = router
        self.sanic.router.apply_routes(self.sanic, self.container)

    def _set_sanic_confs(self):
        self.sanic.config.SWAGGER_UI_CONFIGURATION = {
            "docExpansion": 'none'
        }

    def _configure_sanic_main(self):
        async def on_start(s_app: Sanic):
            for i in range(s_app.state.workers):
                channel = IChannel(f"Channel_{i}")
                setattr(s_app.shared_ctx, f"Channel_{i}", channel)
                self.dispatcher.channels.update({f"Channel_{i}": channel})
                # noinspection PyAsyncCall
                # self.sanic.add_task(channel.listen_produce(self.dispatcher.on_channel_sent))

        self.sanic.main_process_ready(on_start)

    def _configure_sanic_worker(self):
        async def set_worker_ctx(s_app: Sanic):
            # set channel to ctx
            worker_num = int(s_app.m.name.split('-')[-2])
            s_app.ctx.channel = getattr(s_app.shared_ctx, f"Channel_{worker_num}")
            s_app.ctx.container = self.container
            for service, name in s_app.ctx.container.services():
                service.channel = s_app.ctx.channel
            # add addon loader

            # add broadcaster
            s_app.ctx.rt_broadcaster = RtBroadcaster()
            for event, resolver, use_nested_classes in self._rt_listeners:
                s_app.ctx.channel.add_event_listener(
                    event_type=event,
                    callback=partial(s_app.ctx.rt_broadcaster.broadcast, resolve_callback=resolver),
                    use_nested_classes=use_nested_classes)
            await self.container.init_resources(s_app.ctx.channel)
            if hasattr(self.container, "addon_loader") and self.container.addon_loader.initialized:
                await self.container.addon_loader().first_init()

        async def reg_metrics(s_app: Sanic):
            async def give_metric(metric: Metric):
                asyncio.create_task(s_app.ctx.channel.produce(NewMetricEvent(metric)))

            self.sanic.ctx.metrics = SimpleNamespace()

            async def metrics_before(request: Request):
                if not settings.METRICS_ENABLE:
                    return
                request.app.ctx.metrics.exec_time = time.time()

            async def metrics_after(request: Request, response: BaseHTTPResponse):
                if not settings.METRICS_ENABLE:
                    return
                else:
                    metr = HistogramMetric(f"exec_request_time")
                    metr.observe(time.time() - request.app.ctx.metrics.exec_time)
                    metr.add_label(request=request.path,
                                   method=request.method,
                                   status=str(response.status))
                    await give_metric(metr)
                    metr = CounterMetric(f"request_path_count", value=1)
                    metr.add_label(request=request.path,
                                   method=request.method,
                                   status=str(response.status))
                    await give_metric(metr)
                    metr = SummaryMetric(f"request_path_latency")
                    metr.add_label(request=request.path,
                                   method=request.method,
                                   status=str(response.status))
                    metr.observe(time.time() - request.app.ctx.metrics.exec_time)
                    await give_metric(metr)

            self.sanic.register_middleware(metrics_before)
            self.sanic.register_middleware(metrics_after, "response")

        self.sanic.before_server_start(set_worker_ctx)
        self.sanic.before_server_start(reg_metrics)

        async def listen_channel(s_app: Sanic):
            async def on_settings_change(event: SettingsChangeEvent):
                setattr(settings, event.name, event.value)

            s_app.ctx.channel.add_event_listener(SettingsChangeEvent, on_settings_change)
            # noinspection PyAsyncCall
            s_app.add_task(s_app.ctx.channel.listen_consume())

        self.sanic.after_server_start(listen_channel)

        async def on_stop(s_app: Sanic):
            await self.container.shutdown_resources()

        self.sanic.before_server_stop(on_stop)

    # def _add_listener(self, scope: str, listener: AppListener):
    #     if not self.listeners.get(scope):
    #         self.listeners[scope] = []
    #     self.listeners[scope].append(listener)
    #
    # def before_resources_init(self, listener: AppListener):
    #     self._add_listener("before_resource", listener)

    async def before_app_run(self):
        await self.container.before_app_run()

    def run(self):
        asyncio.run(self.before_app_run())
        self._set_sanic_confs()
        self._configure_sanic_main()
        self._configure_sanic_worker()
        sanic_conf = self.container.app_config().sanic
        start_args = sanic_conf.dict() if sanic_conf else {}
        self.sanic.run(**start_args)


AppListener = Callable[[App], None]
