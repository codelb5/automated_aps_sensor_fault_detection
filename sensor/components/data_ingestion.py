import os
from pandas import DataFrame
from sensor.logger import logging
from sensor.utils.main_utils import Utils
from sensor.exceptions import SensorException
from sklearn.model_selection import train_test_split
from sensor.data_access.sensor_data import SensorData
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.constant.database import COLLECTION_NAME

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig)->None:
        try:
            logging.info("Data Ingestion initiated.")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(str(SensorException(error_message=e)))
            raise SensorException(error_message=e)
    
    def import_data_as_feature_store(self,)->DataFrame:
        """
        Description: Import data from mongoDB database and gives a pandas Dataframe.

        Returns: pandas Dataframe.
        """
        try:
            logging.info("Importing data as a feature store.")
            sensor_data = SensorData
            df = sensor_data.import_data_from_mongodb(collection_name=COLLECTION_NAME)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            feature_store_dir = os.path.dirname(feature_store_file_path)
            os.makedirs(name=feature_store_dir, exist_ok= True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            logging.info("File got stored in feature_store as [{0}]".format(
                os.path.basename(feature_store_file_path)
            ))
            return df
        except Exception as e:
            logging.error(str(SensorException(error_message=e)))
            raise SensorException(error_message=e)
        
    def data_split(self, df:DataFrame)->None:
        """
        Description: Perform train test split on the data and store them as train file and test file seperately.
        
        Params:
        --------
        df: DataFrame
            pandas datframe to be split

        """
        try:
            train_data, test_data = train_test_split(
                df, test_size=self.data_ingestion_config.test_split_ratio
            )
            logging.info("Performed train test split on the given dataframe.")
            
            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path
        
            train_file_dir = os.path.dirname(train_file_path)
            os.makedirs(train_file_dir, exist_ok=True)
            
            train_data.to_csv(train_file_path, index=False, header=True)
            logging.info("Train file stored as [{0}]".format(
                os.path.basename(train_file_path)
            ))
            print(train_data.columns)
            print(test_data.columns)
            test_data.to_csv(test_file_path, index=False, header=True
            )
            logging.info("Train file stored as [{0}]".format(
                os.path.basename(test_file_path)
            ))
            logging.info("Train test split completed successfully.")
        
        except Exception as e:
            logging.error(str(SensorException(error_message=e)))
            raise SensorException(error_message=e)
  
    def initiate_data_ingestion(self,)->DataIngestionArtifact:
        try:
            df = self.import_data_as_feature_store()
            # train test split
            self.data_split(df=df)
            
            data_ingestion_artifact = DataIngestionArtifact(
                  feature_store_path=self.data_ingestion_config.feature_store_file_path
                , train_file_path=self.data_ingestion_config.train_file_path
                , test_file_path=self.data_ingestion_config.test_file_path
            )
            
            logging.info("Data Ingestion completed.")
            return data_ingestion_artifact
        except Exception as e:
            logging.error(str(SensorException(error_message=e)))
            raise SensorException(error_message=e)
        

    

