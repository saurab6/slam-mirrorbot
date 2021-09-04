from bot.helper.ext_utils.bot_utils import setInterval
from bot import auto_shutdown_handler,download_dict_lock, download_dict, LOGGER

class NotifyDict(dict):

    def __init__(self, *args, **kwargs):
        LOGGER.info("INIT")
        self.check_if_autoshutdown_possible(60)
        dict.__init__(self, *args, **kwargs)

    def _wrap(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            LOGGER.info("wrap")
            self.check_if_autoshutdown_possible(30)
            return result
        return wrapper
    __delitem__ = _wrap(dict.__delitem__)
    __setitem__ = _wrap(dict.__setitem__)
    clear = _wrap(dict.clear)
    pop = _wrap(dict.pop)
    popitem = _wrap(dict.popitem)
    setdefault = _wrap(dict.setdefault)
    update =  _wrap(dict.update)
    copy =  _wrap(dict.copy)

    def shutdown(self):
        with download_dict_lock:
            if not bool(download_dict):
                LOGGER.info("Shutting down worker to save dyno hours")

    def check_if_autoshutdown_possible(self,interval):
        with download_dict_lock:
            global auto_shutdown_handler
            if not bool(download_dict):
                LOGGER.info("NO DOWNLOADS AVAILABLE")
                if auto_shutdown_handler is None:
                    LOGGER.info("adding schedular")
                    auto_shutdown_handler = setInterval(interval,self.shutdown)
            else:
                LOGGER.info("Downloads still here")
                if auto_shutdown_handler is not None:
                    LOGGER.info("scedular cancelled")
                    auto_shutdown_handler.cancel()
                LOGGER.info("schedular set to None")
                auto_shutdown_handler = None