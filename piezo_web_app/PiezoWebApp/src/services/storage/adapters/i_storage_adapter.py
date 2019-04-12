from abc import ABCMeta, abstractmethod


class IStorageAdapter(metaclass=ABCMeta):

    @abstractmethod
    @property
    def access_protocol(self):
        pass

    @abstractmethod
    def create_bucket(self, bucket_name):
        pass

    @abstractmethod
    def does_bucket_exist(self, bucket_name):
        pass

    @abstractmethod
    def generate_temp_url(self, bucket_name, file_path, expiry_seconds, method):
        pass

    @abstractmethod
    def get_all_files(self, bucket_name, file_prefix):
        pass

    @abstractmethod
    def set_contents_from_string(self, bucket_name, file_path, text):
        pass
