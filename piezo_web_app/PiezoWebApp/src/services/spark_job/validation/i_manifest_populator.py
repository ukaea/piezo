from abc import ABCMeta, abstractmethod


class IManifestPopulator(metaclass=ABCMeta):

    @abstractmethod
    def build_manifest(self, validated_parameters_dict):
        pass
