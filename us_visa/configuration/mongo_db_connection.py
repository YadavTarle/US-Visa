import os 
import sys
from us_visa.constants import DATABASE_NAME,MONGODB_URL_KEY
import pymongo
import certifi
from us_visa.exception import USvisaException
from us_visa.logger import logging


ca = certifi.where() 
# certifi package prevent timeout issue

class MongoDBClient:
    """
    Class Name  : export_data_into_feature_store
    Description : This method exports the dataframe mangodb feature store as dataframe
    
    Output      : connection to mongodb database
    On failue   : raises an exception
    """
    client = None

    def __init__(self,database_name = DATABASE_NAME)-> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception("Environment variable MONGODB_CONNECTION_URL is not set")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"MongoDB client created with database name: {self.database_name}")
        except Exception as e:
            raise USvisaException(e,sys)
