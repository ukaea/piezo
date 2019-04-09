import os.path

import boto.s3.connection

from PiezoWebApp.src.services.storage.adapters.i_storage_adapter import IStorageAdapter


class BotoAdapter(IStorageAdapter):
    def __init__(self, configuration, logger):
        self._logger = logger

        with open(os.path.join(configuration.secrets_dir, 'access_key')) as key_file:
            access_key = key_file.read()
        with open(os.path.join(configuration.secrets_dir, 'secret_key')) as key_file:
            secret_key = key_file.read()
        try:
            self._s3_client = boto.connect_s3(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                host=configuration.s3_host,
                port=configuration.s3_port,
                is_secure=configuration.is_s3_secure,
                calling_format=boto.s3.connection.OrdinaryCallingFormat()
            )
        except Exception as exception:
            self._logger.critical(exception)
            raise exception

        self._temp_url_expiry_seconds = configuration.temp_url_expiry_seconds

    def get_temp_url_for_each_file(self, bucket_name, file_prefix):
        bucket = self._get_bucket(bucket_name)
        keys = bucket.get_all_keys(prefix=file_prefix)
        temp_urls = {key.name: key.generate_url(self._temp_url_expiry_seconds, method='GET') for key in keys}
        return temp_urls

    def set_contents_from_string(self, bucket_name, file_path, text):
        key = self._get_key(bucket_name, file_path)
        contents_size = key.set_contents_from_string(text)
        self._logger.debug(f'Wrote {contents_size} bytes to "{file_path}" in bucket "{bucket_name}"')

    def _get_bucket(self, bucket_name):
        bucket = self._s3_client.lookup(bucket_name)
        if bucket is None:
            raise RuntimeError(f'Bucket "{bucket_name}" does not exist')
        return bucket

    def _get_key(self, bucket_name, file_path):
        bucket = self._get_bucket(bucket_name)
        key = bucket.get_key(file_path)
        if key is None:
            key = bucket.new_key(file_path)
        return key
