from abc import ABCMeta, abstractmethod


class IValidationService(metaclass=ABCMeta):

    @abstractmethod
    def validate_request_keys(self, request_body):
        pass

    @abstractmethod
    def validate_request_values(self, request_body):
        pass
