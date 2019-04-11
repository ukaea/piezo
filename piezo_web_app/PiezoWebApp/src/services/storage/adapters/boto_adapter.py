import boto.s3.connection

from PiezoWebApp.src.services.storage.adapters.i_storage_adapter import IStorageAdapter


class BotoAdapter(IStorageAdapter):
    def __init__(self, access_key, is_s3_secure, s3_host, s3_port, secret_key):
        self._s3_client = boto.connect_s3(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                host=s3_host,
                port=s3_port,
                is_secure=is_s3_secure,
                calling_format=boto.s3.connection.OrdinaryCallingFormat()
            )

    def create_bucket(self, bucket_name):
        self._s3_client.create_bucket(bucket_name, location="")

    def does_bucket_exist(self, bucket_name):
        bucket = self._s3_client.lookup(bucket_name)
        return bucket is not None

    def generate_temp_url(self, bucket_name, file_path, expiry_seconds, method):
        bucket = self._get_bucket(bucket_name)
        key = bucket.get_key(file_path)
        temp_url = key.generate_url(expiry_seconds, method=method)
        return temp_url

    def get_all_files(self, bucket_name, file_prefix):
        bucket = self._get_bucket(bucket_name)
        keys = bucket.get_all_keys(prefix=file_prefix)
        files = [key.name for key in keys]
        return files

    def set_contents_from_string(self, bucket_name, file_path, text):
        key = self._get_key(file_path)
        contents_size = key.set_contents_from_string(text)
        return contents_size

    def _get_bucket(self, bucket_name):
        bucket = self._s3_client.lookup(bucket_name)
        return bucket

    def _get_key(self, file_path):
        key = self._bucket.get_key(file_path)
        if key is None:
            key = self._bucket.new_key(file_path)
        return key
