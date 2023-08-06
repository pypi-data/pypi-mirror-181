import time
import pyhik.hikvision


class CAD:
    def __init__(self, host, login, password, logger, callback_func=None,
                 delay_time=0.5, port=80, catch_event='Line Crossing'):
        # self.cam = Client(host, login, password, timeout=30)
        self.camera = pyhik.hikvision.HikCamera(
            host, port=port,
            usr=login,
            pwd=password)
        self.callback_func = callback_func
        self.delay_time = delay_time
        self.logger = logger
        self.catch_event = catch_event

    def set_callback_func(self, func):
        self.callback_func = func

    def mainloop(self):
        self.logger.info('CAD has started work')
        self.camera.start_stream()
        if not self.callback_func:
            return 'Set callback_function first!'
        while True:
            events = self.camera.current_event_states
            if events and events[self.catch_event][0][0]:
                self.logger.debug("CAD calling back")
                self.callback_func(None)
            time.sleep(1)
