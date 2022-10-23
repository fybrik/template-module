from fybrik_python_logging import logger, Error, DataSetID, ForUser
from fybrik_python_vault import get_jwt_from_file, get_raw_secret_from_vault
import boto3

def s3_connection(endpoint, aws_access_key, aws_secret_key):
    try:
        logger.info("Connecting S3 client")
        s3_resource = boto3.resource("s3", endpoint_url=endpoint, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    except Exception as e:
        logger.error("Could not connect to S3", extra={Error: str(e), ForUser: True})
    else:
        return s3_resource

def delete_object(resource, bucket_name, object_key):
    try:
        logger.info(f"Deleting object: '{object_key}' from bucket: '{bucket_name}'")
        obj = resource.ObjectSummary(bucket_name=bucket_name, key=object_key)
        if obj not in resource.Bucket(bucket_name).objects.all():
            logger.error(f"Couldn't find object key '{object_key}' in bucket '{bucket_name}'")
            return
        obj.delete()
        logger.info(f"Successfully deleted object: '{object_key}'")
    except Exception as e:
        logger.error(f"Could not delete object '{object_key}'",
            extra={Error: str(e), ForUser: True})
        

def delete_bucket_if_empty(resource, bucket_name):
    try:
        logger.info(f"DeleteBucketIfEmpty is true; Checking if bucket '{bucket_name}' is empty")
        bucket = resource.Bucket(bucket_name)
        if not list(bucket.objects.all()):
            bucket.delete()
            logger.info(f"Successfully deleted bucket: '{bucket_name}'")
        else:
            logger.info(f"Bucket '{bucket_name}' is not empty, delete aborted")
    except Exception as e:
        logger.error(f"Could not delete bucket '{bucket_name}'",
            extra={Error: str(e), ForUser: True})

def get_s3_credentials_from_vault(vault_credentials, datasetID):
    jwt_file_path = vault_credentials.get('jwt_file_path', '/var/run/secrets/kubernetes.io/serviceaccount/token')
    jwt = get_jwt_from_file(jwt_file_path)
    vault_address = vault_credentials.get('address', 'https://localhost:8200')
    secret_path = vault_credentials.get('secretPath', '/v1/secret/data/cred')
    vault_auth = vault_credentials.get('authPath', '/v1/auth/kubernetes/login')
    role = vault_credentials.get('role', 'demo')
    logger.trace('getting vault credentials',
        extra={'jwt_file_path': str(jwt_file_path),
               'vault_address': str(vault_address),
               'secret_path': str(secret_path),
               'vault_auth': str(vault_auth),
               'role': str(role),
               DataSetID: datasetID,
               ForUser: True})
    credentials = get_raw_secret_from_vault(jwt, secret_path, vault_address, vault_auth, role, datasetID)
    if not credentials:
        raise ValueError("Vault credentials are missing")
    if 'access_key' in credentials and 'secret_key' in credentials:
        if credentials['access_key'] and credentials['secret_key']:
            return credentials['access_key'], credentials['secret_key']
        else:
            if not credentials['access_key']:
                logger.error("'access_key' must be non-empty",
                             extra={DataSetID: datasetID, ForUser: True})
            if not credentials['secret_key']:
                logger.error("'secret_key' must be non-empty",
                             extra={DataSetID: datasetID, ForUser: True})
    logger.error("Expected both 'access_key' and 'secret_key' fields in vault secret",
                 extra={DataSetID: datasetID, ForUser: True})
    raise ValueError("Vault credentials are missing")
