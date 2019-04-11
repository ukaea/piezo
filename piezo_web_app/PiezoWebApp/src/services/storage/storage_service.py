from PiezoWebApp.src.services.storage.i_storage_service import IStorageService


class StorageService(IStorageService):
    def __init__(self, configuration, logger, storage_adapter):
        self._bucket_name = configuration.s3_bucket_name
        self._temp_url_expiry_seconds = configuration.temp_url_expiry_seconds
        self._logger = logger
        self._storage_adapter = storage_adapter

        self._set_up_bucket(self._bucket_name)

    def get_temp_url_for_each_file(self, file_prefix):
        files = self._storage_adapter.get_all_files(self._bucket_name, file_prefix)
        urls = {
            file_path: self._storage_adapter.generate_temp_url(
                self._bucket_name, file_path, self._temp_url_expiry_seconds, 'GET'
            )
            for file_path in files
        }
        self._logger.debug(f'Generated temporary GET URLs for {len(files)} files in "{file_prefix}"')
        return urls

    def set_contents_from_string(self, file_path, text):
        contents_size = self._storage_adapter.set_contents_from_string(self._bucket_name, file_path, text)
        self._logger.debug(f'Wrote {contents_size} bytes to "{file_path}"')

    def _set_up_bucket(self, bucket_name):
        if self._storage_adapter.does_bucket_exist(bucket_name):
            self._logger.info(f'Bucket "{bucket_name}" already exists: no need to change')
        else:
            self._storage_adapter.create_bucket(bucket_name)
            self._logger.info(f'Created new bucket "{bucket_name}"')
