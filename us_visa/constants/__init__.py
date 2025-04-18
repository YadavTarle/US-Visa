import os
from datetime import date

DATABASE_NAME = "US_VISA"

COLLECTION_NAME = "EasyVisa"

MONGODB_URL_KEY = "MONGODB_URL"


PIPELINE_NAME: str = "usvisa"

ARTIFACT_DIR: str = "artifact"

FILE_NAME:str = "EasyVisa.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.abspath(r"D:\US_visaProject\US-Visa\config\schema.yaml")
#SCHEMA_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "schema.yaml")

"""
Data Ingestion related constants start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "EasyVisa"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation related constants starts with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
