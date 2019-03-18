import boto.s3.connection

from PiezoWebApp.src.services.storage.adapters.i_storage_adapter import IStorageAdapter


class BotoAdapter(IStorageAdapter):
    def __init__(self, configuration, logger):
        self._logger = logger
        try:
            self._s3_client = boto.connect_s3(
                aws_access_key_id=configuration.s3_access_key,
                aws_secret_access_key=configuration.s3_secret_key,
                host=configuration.s3_host,
                port=configuration.s3_port,
                is_secure=configuration.s3_use_secure,
                calling_format=boto.s3.connection.OrdinaryCallingFormat()
            )
        except Exception as exception:
            self._logger.critical(exception)
            raise exception

    def set_contents_from_string(self, bucket_name, file_path, text):
        key = self._get_key(bucket_name, file_path)
        key.set_contents_from_string

    def _get_bucket(self, bucket_name):
        bucket = self._s3_client.lookup(bucket_name)
        if bucket is None:
            raise RuntimeError(f'Bucket "{bucket_name}" does not exist')
        return bucket

    def _get_key(self, bucket_name, file_path):
        bucket = self._get_bucket(bucket_name)
        key = bucket.get_key(file_path)
        return key
