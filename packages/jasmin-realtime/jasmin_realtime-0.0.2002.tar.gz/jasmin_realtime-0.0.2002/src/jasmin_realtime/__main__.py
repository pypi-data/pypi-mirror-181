import sys
from .realtime import Realtime
sys.argv.pop(0)

arguments:dict[str, str] = {}

for arg in sys.argv:
    argument = arg.split('=',1)
    if len(argument) > 1:
        arguments[argument[0]] = argument[1]


realtime = Realtime()
if "--amqp-host" in arguments and "--amqp-port" in arguments:
    realtime.initiate_amqb(host=arguments["--amqp-host"], port=int(arguments["--amqp-port"]))

if "--mongo-connection" in arguments:
    realtime.initiate_mongodb(connection_string=arguments["--mongo-connection"])

if "--log-db" in arguments and "--log-col" in arguments:
    realtime.initiate_logger(database=arguments["--log-db"], collection=arguments["--log-col"])
    
realtime.start()


# # AMQB broker connection parameters
# amqp_broker_host = os.getenv('AMQP_BROKER_HOST', '127.0.0.1')
# amqp_broker_port = int(os.getenv('AMQP_BROKER_PORT', '5672'))

# mongodb_ready = os.getenv("MONGODB_CONNECTION_STRING") is not None

# log_ready = mongodb_ready is True and \
#     os.getenv("MONGODB_LOGS_DATABASE") is not None and \
#     os.getenv("MONGODB_LOGS_COLLECTION") is not None

# config_ready = mongodb_ready is True and \
#     os.getenv("MONGODB_MODULES_DATABASE") is not None

# J_CLI_CONN = {
#     "host": os.getenv("JASMIN_CLI_HOST", "127.0.0.1"),
#     "port": int(os.getenv("JASMIN_CLI_PORT", "8990")),
#     "buffer_time": int(os.getenv("JASMIN_CLI_BUFFER_TIME", "500000")),
#     "timeout": int(os.getenv("JASMIN_CLI_TIMEOUT", "30")),
#     "username": os.getenv("JASMIN_CLI_USERNAME", "jcliadmin"),
#     "password": os.getenv("JASMIN_CLI_PASSWORD", "jclipwd"),
#     "standard_prompt": os.getenv("JASMIN_CLI_STANDARD_PROMPT", "jcli : "),
#     "interactive_prompt": os.getenv("JASMIN_CLI_INTERACTIVE_PROMPT", "> "),
#     "shared_temp": os.getenv("JASMIN_CLI_SHARED_TEMP", "/tmp/")
# }

# MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")

# MONGODB_LOGS_DATABASE = os.getenv("MONGODB_LOGS_DATABASE", "logs")
# MONGODB_LOGS_COLLECTION = os.getenv("MONGODB_LOGS_COLLECTION", "sms_log")

# MONGODB_MODULES_DATABASE = os.getenv("MONGODB_MODULES_DATABASE", "modules")

# MONGODB_BILL_DATABASE = os.getenv(
#     "MONGODB_BILL_DATABASE", MONGODB_MODULES_DATABASE)
# MONGODB_BILL_COLLECTION = os.getenv("MONGODB_BILL_COLLECTION", "user")
# MONGODB_BILL_BALANCE_KEY = os.getenv(
#     "MONGODB_BILL_BALANCE_KEY", "mt_messaging_cred quota balance")

