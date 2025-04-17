import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name  : start_data_ingestion
        Description : This method starts the data ingestion process.
        
        Output      : data is returned as artifact of data ingestion component
        On failure   : raises an exception
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainingPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from the mongodb")
            logging.info("Exited the start_data_ingestion method of TrainingPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
    def run_pipeline(self,) -> None:
        """
        Method Name  : run_pipeline
        Description : This method runs the entire training pipeline.
        
        Output      : None
        On failure   : raises an exception
        """
        try:
            logging.info("Entered the run_pipeline method of TrainingPipeline class")
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info("Exited the run_pipeline method of TrainingPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e