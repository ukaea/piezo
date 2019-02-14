from PiezoWebApp.src.services.application_builder.default_template import DefaultTemplate


class TemplatePopulator:

    def build_template(self, validated_parameters_dict):
        template = DefaultTemplate().create_template()
        template["metadata"]["name"] = validated_parameters_dict["name"]
        template["spec"]["mainApplicationFile"] = validated_parameters_dict["path_to_main_application_file"]
        template["spec"]["driver"]["cores"] = validated_parameters_dict["driver_cores"]
        template["spec"]["driver"]["coreLimit"] = validated_parameters_dict["driver_core_limit"]
        template["spec"]["driver"]["memory"] = validated_parameters_dict["driver_memory"]
        template["spec"]["executor"]["instances"] = validated_parameters_dict["executors"]
        template["spec"]["executor"]["cores"] = validated_parameters_dict["executor_cores"]
        template["spec"]["executor"]["memory"] = validated_parameters_dict["executor_memory"]

        if validated_parameters_dict["language"].lower() == "python":
            return self._populate_python_job_template(template, validated_parameters_dict)
        return self._populate_scala_job_template(template, validated_parameters_dict)

    @staticmethod
    def _populate_python_job_template(template, validated_parameters_dict):
        template["spec"]["type"] = "Python"
        template["spec"]["pythonVersion"] = validated_parameters_dict["pythonVersion"]

    @staticmethod
    def _populate_scala_job_template(template, validated_parameters_dict):
        template["spec"]["type"] = "Scala"
        template["spec"]["mainClass"] = validated_parameters_dict["main_class"]
        return template
