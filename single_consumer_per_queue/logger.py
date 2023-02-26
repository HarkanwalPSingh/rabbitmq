from logging import getLogger, getLevelName, Formatter, StreamHandler

class Logger:
    def __init__(self, cls) -> None:
        self.log = getLogger(cls)
        self.log_formatter = Formatter("%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s ")
        self.console_handler = StreamHandler()
        self.console_handler.setFormatter(self.log_formatter)
        self.log.addHandler(self.console_handler)
        self._loggerTypes = {
            "CRITICAL" : 50,
            "FATAL" : 50,
            "ERROR" : 40,
            "WARNING" : 30, 
            "WARN" : 30,
            "INFO" : 20,
            "DEBUG" : 10,
            "NOTSET" : 0,
        }
    
    def getLogger(self, logger_type):
        if logger_type not in self._loggerTypes:
            raise TypeError("Not supported logger type")
        self.log.setLevel(getLevelName(self._loggerTypes.get(logger_type)))
        return self.log

        
