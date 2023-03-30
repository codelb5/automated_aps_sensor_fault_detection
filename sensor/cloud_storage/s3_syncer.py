import os
from sensor.logger import logging
from sensor.exceptions import SensorException
class S3Sync:
    @staticmethod
    def sync_folder_to_s3(folder:str, aws_bucket_url:str)->None:
        try:
            s3_command = f"aws s3 sync {folder} {aws_bucket_url}"
            os.system(command=s3_command)
            logging.info("Folder synced to S3 bucket.")
        except Exception as e:
            logging.error(str(SensorException(error_message=e)))
            raise SensorException(error_message=e)
    
    @staticmethod
    def sync_folder_from_s3(folder:str, aws_bucket_url:str)->None:
        try:
            s3_command = f"aws s3 sync {aws_bucket_url} {folder}"
            os.system(command=s3_command)
            logging.info("Folder synced from S3 bucket.")
        except Exception as e:
            logging.error(str(SensorException(error_message=e)))
            raise SensorException(error_message=e)
        
