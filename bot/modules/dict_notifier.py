from bot.helper.ext_utils.bot_utils import setInterval
from bot import auto_shutdown_handler, download_dict, LOGGER

class NotifyDict(dict):

    def __init__(self, *args, **kwargs):
        self.check_if_autoshutdown_possible(60)
        dict.__init__(self, *args, **kwargs)

    def _wrap(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
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
        if not bool(download_dict):
            LOGGER.info("Shutting down worker to save dyno hours")

    def check_if_autoshutdown_possible(self,interval):
        global auto_shutdown_handler
        if not bool(download_dict):
            LOGGER.info("NO DOWNLOADS AVAILABLE")
            if auto_shutdown_handler is None:
                auto_shutdown_handler = setInterval(interval,self.shutdown)
        else:
            if auto_shutdown_handler is not None:
                auto_shutdown_handler.cancel()
            auto_shutdown_handler = None
