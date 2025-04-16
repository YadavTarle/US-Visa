import os
from datetime import date

DATABASE_NAME = "US_VISA"

COLLECTION_NAME = "EasyVisa"

MANGODB_URL_KEY = "MONGODB_CONNECTION_URL"


PIPELINE_NAME: str = "usvisa"

ARTIFACT_DIR: str = "artifact"

FILE_NAME:str = "EasyVisa.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

MODEL_FILE_NAME = "model.pkl"

"""
Data Ingestion related constants start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "EasyVisa"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
