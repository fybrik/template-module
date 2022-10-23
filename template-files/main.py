from module.config import Config
from module.s3 import s3_connection, delete_bucket_if_empty, delete_object, get_s3_credentials_from_vault
from fybrik_python_logging import init_logger, logger


if __name__ == "__main__":
    init_logger("INFO", "", 'delete-module')
    logger.info('Delete module initialized')

    conf = Config("/etc/conf/conf.yaml")
    conf_data = conf.values["data"][0]
    dataID = conf_data["name"]
    endpoint = conf_data["connection"]["s3"]["endpoint_url"]
    vault_cred = conf_data["connection"]["s3"]["vault_credentials"]
    bucket_name, object_key = conf_data["path"].split("/")

    access_key, secret_key = get_s3_credentials_from_vault(vault_cred, dataID)

    s3_resource = s3_connection(endpoint, access_key, secret_key)

    delete_object(s3_resource, bucket_name, object_key)
    delete_empty_bucket = False # will be set to get the vaule form configmap when fybrik will have that feature
    if delete_empty_bucket:
        delete_bucket_if_empty(s3_resource, bucket_name)








