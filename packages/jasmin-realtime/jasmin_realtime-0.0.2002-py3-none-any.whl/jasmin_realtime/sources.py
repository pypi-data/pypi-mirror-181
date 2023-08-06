from pymongo import MongoClient, errors as MongoErrors
from pymongo.database import Database as MongoDatabase
from jasmin_telnet.proxy import Proxy as JasminTelnetProxy
from .settings import *

import logging

class MongoDB:

    def __init__(self, database_name):
        """ Constructor """
        self.database_name = database_name
        logging.basicConfig(level=logging.DEBUG, filename="jasmin_realtime.source.MongoDB", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
        logging.info("Starting ::MongoDB Socket::")

    def logger_callback(self, msg:str):
        logging.info(msg=msg)

    def startConnection(self) -> bool:
        mongoclient = MongoClient(MONGODB_CONNECTION_STRING)
        server_info = mongoclient.server_info()
        if isinstance(server_info, dict) and 'ok' in server_info and server_info['ok'] == 1:
            logging.info("Connected to MongoDB")
            self.mongoclient = mongoclient
            database: MongoDatabase = self.mongoclient[self.database_name]
            database_info = database.command("buildinfo")
            if isinstance(database_info, dict) and 'ok' in database_info and database_info['ok'] == 1:
                logging.info(f"Set to use database: {self.database_name}")
                logging.info("")
                self.database = database
                return True
            else:
                logging.critical(f"Failed to use database: {self.database_name}")
                return False
        else:
            logging.critical("Failed to connect to MongoDB")
            return False

    def get_one_module(self, module: str) -> dict[str, str | float | bool]:
        "" ""
        data: dict[str, str | float | bool] = {}
        cursor = self.database[module].find()
        for row in cursor:
            sub_id = row["_id"]
            del row["_id"]
            data[sub_id] = row

        return data

    def get_one_submodule(self, module: str, sub_id: str) -> dict[str, str | float | bool]:
        "" ""
        return self.database[module].find_one({"_id": sub_id})

    def insert_one(self, module, sub_id, data):
        data["_id"] = sub_id
        self.database[module].insert_one(data)

    def increment_one(self, module, sub_id, data):
        self.database[module].update_one(
            {"_id": sub_id}, {'$inc': data})

    def update_one(self, module, sub_id, data, upsert=True):
        self.database[module].update_one(
            {"_id": sub_id}, {'$set': data}, upsert=upsert)

    def pullAllConfigurations(self):
        "" ""
        sync_data = {
            "smppccm": {},
            "httpccm": {},
            "group": {},
            "user": {},
            "filter": {},
            "mointerceptor": {},
            "mtinterceptor": {},
            "morouter": {},
            "mtrouter": {},
        }

        for module in sync_data.keys():
            cursor = self.database[module].find()
            for row in cursor:
                sub_id = row["_id"]
                del row["_id"]
                sync_data[module][sub_id] = row

        self.stream_handler(payload={
            "change_type": "sync",
            "sync_data": sync_data
        })

    def stream(self, syncCurrentFirst: bool = False):
        self.syncCurrentFirst = syncCurrentFirst
        try:
            with self.database.watch(full_document='updateLookup') as stream:
                logging.info("Started listening to config sever!")
                logging.info("")

                if self.syncCurrentFirst is True:
                    # Sync current data to Jasmin before waiting for changes
                    self.pullAllConfigurations()

                for change in stream:
                    module = change["ns"]["coll"]
                    sub_id = change["documentKey"]["_id"]
                    change_type = change["operationType"]
                    if change_type == "invalidate":
                        return
                    if change_type in ["create", "drop", "dropDatabase", "rename", "modify"]:
                        self.pullAllConfigurations()
                        continue
                    if "updateDescription" in change and module in ["user", "smppccm"]:
                        sub_data = change["updateDescription"]["updatedFields"]
                    elif "fullDocument" in change:
                        sub_data = change["fullDocument"]
                    else:
                        sub_data = {}

                    if isinstance(sub_data, dict) and "_id" in sub_data:
                        del sub_data["_id"]

                    self.stream_handler(payload={
                        "module": module,
                        "sub_id": sub_id,
                        "change_type": change_type,
                        "sub_data": sub_data
                    })
        except MongoErrors.PyMongoError as err:
            # The ChangeStream encountered an unrecoverable error or the
            # resume attempt failed to recreate the cursor.
            logging.error(err)
            pass
        except KeyboardInterrupt:
            pass

    def stream_handler(self, payload):
        """Handle callback for jasmin stream"""
        jasmin_proxy = JasminTelnetProxy(
            host=J_CLI_CONN["host"],
            port=J_CLI_CONN["port"],
            timeout=J_CLI_CONN["timeout"],
            username=J_CLI_CONN["username"],
            password=J_CLI_CONN["password"],
            standard_prompt=J_CLI_CONN["standard_prompt"],
            interactive_prompt=J_CLI_CONN["interactive_prompt"],
            log_status=True,
            logger=self.logger_callback
        )
        if hasattr(self, "syncCurrentFirst"):
            if isinstance(self.syncCurrentFirst, bool) and self.syncCurrentFirst is True:
                logging.info("Fresh connection. Sync all configurations")
                self.syncCurrentFirst = False
            else:
                logging.info("Recieved notice of change in configurations")

            logging.info("from source. Applies to:")
        if payload["change_type"] == "sync" and "sync_data" in payload:
            """ Sync """
            jasmin_proxy.syncAll(
                collection_data=payload["sync_data"]
            )

        if payload["change_type"] == "insert":
            """ Add """
            jasmin_proxy.add(
                module=payload["module"],
                sub_id=payload["sub_id"],
                options=payload["sub_data"]
            )

        if payload["change_type"] in ["update", "replace"]:
            """ Edit """
            jasmin_proxy.edit(
                module=payload["module"],
                sub_id=payload["sub_id"],
                options=payload["sub_data"]
            )

        if payload["change_type"] == "delete":
            """ Remove """
            jasmin_proxy.remove(
                module=payload["module"],
                sub_id=payload["sub_id"]
            )

        logging.info("Finished applying configurations")
