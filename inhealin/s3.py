import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import secrets
from django.conf import settings



AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
AWS_S3_SIGNATURE_VERSION = settings.AWS_S3_SIGNATURE_VERSION
AWS_S3_REGION_NAME = settings.AWS_S3_REGION_NAME
AWS_S3_FILE_OVERWRITE = settings.AWS_S3_FILE_OVERWRITE
AWS_DEFAULT_ACL = settings.AWS_DEFAULT_ACL
AWS_S3_VERIFY = settings.AWS_S3_VERIFY
DEFAULT_FILE_STORAGE = settings.DEFAULT_FILE_STORAGE


def create_presigned_url():
    # Choose AWS CLI profile, If not mentioned, it would take default
    # boto3.setup_default_session(profile_name='personal')
    raw_bytes = secrets.token_bytes(16)
    object_name = raw_bytes.hex()+".pdf"

    # Generate a presigned URL for the S3 object
    bucket_name =  "inhealin-therapist-resumes"
    # object_name="random file name"
    expiration=600
    s3_client = boto3.client('s3', region_name=AWS_S3_REGION_NAME, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, config=boto3.session.Config(signature_version='s3v4'))
    try:
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name,
                # "Content-Disposition": "inline"
                },
                ExpiresIn=expiration)
    except Exception as e:
        print(e)
        logging.error(e)
        return "Error"
    # The response contains the presigned URL
    print(response)
    return response


# create_presigned_url('devopsjunction','sqscli-windows.zip',600)