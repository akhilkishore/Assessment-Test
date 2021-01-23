import boto3
from botocore.exceptions import NoCredentialsError
import awc_config
import functions 
import custom_errors as CustomErrors


def upload_to_aws(local_file, s3_file, upload_now):
    """
        Upload give csv path into AWS S3 with a filename

        Parameters
        ----------
        local_file (string):
            Absolute path of csv file
        s3_file (string):
            File name used to save in AWS S3
        upload_now (boolean):
            Whether to push/upload csv or not
            upload_now is False in default    

        Returns
        -------
        Return nothing.


    """
    if upload_now == True:
        try:
            s3 = boto3.client('s3', aws_access_key_id=awc_config.ACCESS_KEY,
                        aws_secret_access_key=awc_config.SECRET_KEY)
        except:
            functions.add_info_log("Error connecting the AWS S3")
            raise CustomErrors.UnableToConnectToS3
        try:
            s3.upload_file(local_file, awc_config.bucket_name, s3_file)
            functions.add_info_log("Upload to AWS S3 successful")
        except FileNotFoundError:
            functions.add_info_log("File not found to upload to AWS S3")
        except NoCredentialsError:
            functions.add_info_log("Credentials not found to upload to AWS S3")
    else :
        functions.add_info_log("Upload to AWS cancelled! ")


