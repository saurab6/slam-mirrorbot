import threading
import time
from bot import bot, OWNER_ID, auto_shutdown_handler, LOGGER, HEROKU_API_KEY, HEROKU_APP_NAME, AUTO_SHUTDOWN_INTERVAL, AUTO_SHUTDOWN
import heroku3

class setInterval:
    def __init__(self, interval, action, repeat = True):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        self.repeat = repeat
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()
            if not self.repeat:
                break

    def cancel(self):
        self.stopEvent.set()

class NotifyDict(dict):

    def __init__(self, *args, **kwargs):
        LOGGER.info("INIT")
        if AUTO_SHUTDOWN and AUTO_SHUTDOWN_INTERVAL is not None:
            self.heroku_app = None
            self.heroku_connect = None
            try:
                self.heroku_connect = heroku3.from_key(HEROKU_API_KEY)
                self.heroku_app = self.heroku_connect.apps()[HEROKU_APP_NAME]
                LOGGER.info("Connected to heroku account successfully")
            except:
                LOGGER.info("Can't Connect to heroku account. Please check your heroku credentials")
                LOGGER.info("Without heroku credentials, AutoShutDown will not work")
            if self.heroku_app is not None:
                self.check_if_autoshutdown_possible(AUTO_SHUTDOWN_INTERVAL)
        dict.__init__(self, *args, **kwargs)
    
    def _wrap(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            if AUTO_SHUTDOWN and AUTO_SHUTDOWN_INTERVAL is not None and self.heroku_app is not None:
                self.check_if_autoshutdown_possible(AUTO_SHUTDOWN_INTERVAL)
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
        if not bool(self) and AUTO_SHUTDOWN and AUTO_SHUTDOWN_INTERVAL is not None and self.heroku_app is not None:
            LOGGER.info("Shutting down to save dyno hours")
            bot.send_message(chat_id=OWNER_ID,text="Shutting down to save dyno hours")
            for p in self.heroku_app.process_formation():
                p.scale(0)

    def check_if_autoshutdown_possible(self,interval):
        global auto_shutdown_handler
        if not bool(self):
            LOGGER.info("NO DOWNLOADS AVAILABLE")
            if auto_shutdown_handler is None:
                auto_shutdown_handler = setInterval(interval,self.shutdown,repeat=False)
                LOGGER.info("Added Scheduler")
        else:
            LOGGER.info("Downloads are present")
            if auto_shutdown_handler is not None:
                auto_shutdown_handler.cancel()
                LOGGER.info("Scheduler cancelled")
            auto_shutdown_handler = None
            LOGGER.info("Scheduler set to None")
