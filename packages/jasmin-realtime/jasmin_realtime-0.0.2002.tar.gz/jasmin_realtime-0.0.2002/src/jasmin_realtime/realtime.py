from .logger import Logger
import logging
import threading


class Realtime:
    def __init__(self):
        self.amqb_initiated = False
        self.telnet_initiated = False
        self.mongodb_initiated = False
        self.logger_initiated = False
        self.moduler_initiated = False
        self.biller_initiated = False
        logging.basicConfig(level=logging.DEBUG, filename="jasmin_realtime", filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
        logging.info("*********************************************")
        logging.info("::Jasmin Realtime Moduler, Biller, and Logger::")
        pass

    def moduler_log(self):
        pass

    def biller_log(self):
        pass

    def logger_log(self):
        pass

    def initiate_amqb(self, host: str = "127.0.0.1", port: int = 5672):
        self.AMQP_BROKER_HOST = host
        self.AMQP_BROKER_PORT = port
        self.amqb_initiated = True

    def initiate_telnet(self, host: str = "127.0.0.1", port: int = 8990, timeout: int = 10, auth: bool = True, username: str = "jcliadmin", password: str = "jclipwd", standard_prompt: str = "jcli : ", interactive_prompt: str = "> "):
        self.TELNET_HOST = host
        self.TELNET_PORT = port
        self.TELNET_TIMEOUT = timeout
        self.TELNET_AUTH = auth
        self.TELNET_USERNAME = username
        self.TELNET_PASSWORD = password
        self.TELNET_STANDARD_PROMPT = standard_prompt
        self.TELNET_INTERACTIVE_PROMPT = interactive_prompt
        self.telnet_initiated = True

    def initiate_mongodb(self, connection_string: str):
        self.MONGODB_CONNECTION_STRING = connection_string
        self.mongodb_initiated = True

    def initiate_logger(self, database: str, collection: str):
        self.MONGODB_LOGS_DATABASE = database
        self.MONGODB_LOGS_COLLECTION = collection
        self.logger_initiated = True

    def initiate_moduler(self, database: str):
        self.MONGODB_MODULES_DATABASE = database
        self.moduler_initiated = True

    def initiate_biller(self, database: str, collection: str, balance_key: str):
        self.MONGODB_BILL_DATABASE = database
        self.MONGODB_BILL_COLLECTION = collection
        self.MONGODB_BILL_BALANCE_KEY = balance_key
        self.biller_initiated = True

    def start(self):
        logger_ready = self.amqb_initiated and self.mongodb_initiated and self.logger_initiated
        biller_ready = self.amqb_initiated and self.mongodb_initiated and self.biller_initiated
        moduler_ready = self.telnet_initiated and self.mongodb_initiated and self.moduler_initiated

        logging.info("Starting up")
        logging.info("")
        if not logger_ready and not biller_ready and not moduler_ready:
            logging.info("Sorry no mode was initiated!")
            logging.info("Shutting Down!!")
            logging.info("*********************************************")
            return

        if moduler_ready:
            logging.info("   - Moduler initiated!")

        if biller_ready:
            logging.info("   - Biller initiated!")

        if logger_ready:
            logging.info("   - Logger initiated!")

        if logger_ready:
            # start logging
            threading.Thread(target=self.start_logger).start()
            pass

        if biller_ready:
            # start billing
            pass

        if moduler_ready:
            # start ConfigurationsWatcher
            pass

    def start_logger(self):
        while True:
            try:
                Logger(amqp_host=self.AMQP_BROKER_HOST, amqp_port=self.AMQP_BROKER_PORT,
                       log_database=self.MONGODB_LOGS_DATABASE, log_collection=self.MONGODB_LOGS_COLLECTION)
            except Exception:
                pass
