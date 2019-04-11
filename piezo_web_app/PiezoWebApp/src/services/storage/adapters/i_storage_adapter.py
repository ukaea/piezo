from abc import ABCMeta, abstractmethod


class IStorageAdapter(metaclass=ABCMeta):

    @abstractmethod
    def get_temp_url_for_each_file(self, bucket_name, file_prefix):
        pass

    @abstractmethod
    def set_contents_from_string(self, bucket_name, file_path, text):
        pass
