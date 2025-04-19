import json
import sys
import pandas as pd
from pandas import DataFrame

# from evidently.model_profile.sections import DataDriftProfileSection
from evidently.metrics import DataDriftTable
from evidently.report import Report
# from evidently.profile import Profile

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file,write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact statge
        :param data_validataion_config:configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path = SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e,sys) from e
    def validate_number_of_columns(self,dataframe : DataFrame)-> bool:
        """
        Method Name : validate_number_of_columns
        Description : Validate the number of columns in the dataframe
        
        Output : True if the number of columns is same as expected, else False
        On Failure : Raise USvisaException
        """
        try : 
            status = len(dataframe.columns) == len(self._schema_config['columns'])
            logging.info(f"Is required number of columns present : {status}")
            return status
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    def is_column_exist(self,df: DataFrame) -> bool:
        """
        Method Name : is_column_exist
        Description : Validate the columns in the dataframe
        
        Output : True if the columns are same as expected, else False
        On Failure : Raise USvisaException
        """
        try: 
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config['numerical_columns']:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical columns : {missing_numerical_columns}")
            
            for column in self._schema_config['categorical_columns']:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            
            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical columns : {missing_categorical_columns}")
            
            return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns)>0 else True
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    @staticmethod
    def read_data(file_path) -> DataFrame:
        """
        Method Name : read_data
        Description : Read the data from the file path
        
        Output : Dataframe of the data read from the file path
        On Failure : Raise USvisaException
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e,sys) from e
        
    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        try:
            report = Report(metrics=[DataDriftTable()])
            report.run(reference_data=reference_df, current_data=current_df)
            drift_report = report.as_dict()

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=drift_report)

            drift_status = drift_report["metrics"][0]["result"]["dataset_drift"]
            return drift_status
        except Exception as e:
            raise USvisaException(e, sys) from e
    

            
    def initiate_data_validation(self)-> DataValidationArtifact:
        """
        Method Name : initiate_data_validation
        Description : Initiate the data validation component for the pipeline

        Output : Return bool value based on validataion results
        On Failure : Raise USvisaException
        """
        
        try: 
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df,test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                DataValidation.read_data(file_path=self.data_ingestion_artifact.testing_file_path))
            
            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns are present in training dataframe : {status}")
            if not status:
                validation_error_msg += "Training data is missing columns\n"
            status = self.validate_number_of_columns(dataframe=test_df)
            logging.info(f"All required columns are present in testing dataframe : {status}")
            if not status:
                validation_error_msg += "Testing data is missing columns\n"

            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg += "Training data is missing columns\n"
            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += "Testing data is missing columns\n"
            
            validation_status = len(validation_error_msg)== 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df,test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg += "Drift detected\n"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"validation_error :{validation_error_msg}")
            
            data_validation_artifact = DataValidationArtifact(
                validation_status = validation_status,
                message = validation_error_msg,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:  
            raise USvisaException(e,sys) from e
                
            
            

