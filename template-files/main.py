from module.config import Config
from module.s3 import s3_connection, get_s3_credentials_from_vault
from fybrik_python_logging import init_logger, logger


if __name__ == "__main__":
    init_logger("INFO", "", 'template-module')
    logger.info('Template module initialized')

    conf = Config("/etc/conf/conf.yaml")
    conf_data = conf.values["data"][0]
    dataID = conf_data["name"]
    endpoint = conf_data["connection"]["s3"]["endpoint_url"]
    vault_cred = conf_data["connection"]["s3"]["vault_credentials"]
    bucket_name, object_key = conf_data["path"].split("/")

    access_key, secret_key = get_s3_credentials_from_vault(vault_cred, dataID)

    s3_resource = s3_connection(endpoint, access_key, secret_key)

    logger.info(f"Configuration data: '{conf_data}'")

    logger.info("Successfully done")









