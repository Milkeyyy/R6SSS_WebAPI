from os import getenv

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from logger import logger


def connect() -> None:
	global collection
	#global collection_checked

	logger.debug("データベースへ接続")

	uri = getenv("MTSCHED_DB_URI")
	# Create a new client and connect to the server
	client = MongoClient(uri, server_api=ServerApi('1'))
	# Access database
	mydatabase = client[getenv("MTSCHED_DB_DATABASE")]
	collection = mydatabase.get_collection(getenv("MTSCHED_DB_COLLECTION"))
	#collection_checked = mydatabase.get_collection(getenv("MTSCHED_DB_COLLECTION_CHECKED"))
