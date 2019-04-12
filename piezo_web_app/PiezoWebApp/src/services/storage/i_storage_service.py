from abc import ABCMeta, abstractmethod


class IStorageService(metaclass=ABCMeta):

    @abstractmethod
    def protocol_route_to_bucket(self):
        pass

    @abstractmethod
    def get_temp_url_for_each_file(self, file_prefix):
        pass

    @abstractmethod
    def set_contents_from_string(self, file_path, text):
        pass
