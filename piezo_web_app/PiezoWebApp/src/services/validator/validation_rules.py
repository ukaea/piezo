class ValidationRules:

    def __init__(self):
        '''
        Validation rules are provided in a dictionary where each key maps to an array of validation values
        in the format:
        [min, max, default, format]
        '''
        self._validation_dict = {"name": [None, None, None, "string"],
                                 "language": [None, None, "Python", "string"],
                                 "python_version": [None, None, "2", "string"],
                                 "main_class": [None, None, None, "string"],
                                 "path_to_main_app_file": [None, None, None, "string"],
                                 "driver_cores": [0.1, 1, 0.1, "float"],
                                 "driver_core_limit": [0.2, 1.2, 0.2, "float"],
                                 "driver_memory": [512, 2048, 512, "int"],
                                 "executors": [1, 10, 1, "int"],
                                 "executor_cores": [1, 4, 1, "float"],
                                 "executor_memory": [512, 4096, 512, "int"]
                                 }

    def get_keys_property_array(self, key):
        return self._validation_dict[key]
