from abc import ABCMeta, abstractmethod


class IStorageAdapter(metaclass=ABCMeta):

    @abstractmethod
    def set_contents_from_string(self, bucket_name, file_path, text):
        pass
