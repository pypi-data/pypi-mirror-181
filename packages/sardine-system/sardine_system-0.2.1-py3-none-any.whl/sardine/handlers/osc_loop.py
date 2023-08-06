from osc4py3.as_eventloop import osc_process, osc_startup, osc_terminate

from ..base import BaseRunnerHandler, BaseThreadedLoopMixin

__all__ = ("OSCLoop",)


class OSCLoop(BaseThreadedLoopMixin, BaseRunnerHandler):
    def __init__(self, *, loop_interval: float = 0.001):
        super().__init__(loop_interval=loop_interval)

    def before_loop(self):
        osc_startup()

    def loop(self):
        osc_process()

    def after_loop(self):
        osc_terminate()
