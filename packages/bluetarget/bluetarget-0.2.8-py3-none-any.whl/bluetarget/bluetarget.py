

from typing import Any, Dict, List, Tuple

import click
from bluetarget.model_version import ModelVersion

from bluetarget.validation import validate_files, validate_model_class

from bluetarget.utils import clean_tmp, prepare_package
from bluetarget.model import Model


class BlueTarget:

    api_key: str
    model_id: str
    model_version_id: str

    environment: Dict = None
    metadata: Dict = None
    implementation: str = "py38"
    framework: str = None
    algorithm: str = None
    tag: str = None
    model_type: str = None

    model: Model

    def __init__(self, api_key: str, model_id: str = None, model_version_id: str = None) -> None:
        self.api_key = api_key
        self.model_id = model_id
        self.model_version_id = model_version_id

        self.model = Model(api_key)

    def set_model_id(self, model_id: str) -> None:
        self.model_id = model_id
        self.model.set_model_id(model_id)

    def set_model_version_id(self, model_version_id: str) -> None:
        self.model_version_id = model_version_id

    def set_environment(self, environment: Dict) -> None:
        self.environment = environment

    def set_metadata(self, metadata: Dict) -> None:
        self.metadata = metadata

    def set_framework(self, framework: str) -> None:
        self.framework = framework

    def set_algorithm(self, algorithm: str) -> None:
        self.algorithm = algorithm

    def set_model_type(self, model_type: str) -> None:
        self.model_type = model_type

    def set_model_version_tag(self, tag: str) -> None:
        self.tag = tag

    def set_implementation(self, implementation: Dict) -> None:
        self.implementation = implementation

    def retrieve_optional_parameters(self, **kwargs) -> Dict[str, Any]:

        metadata = kwargs.pop("metadata", self.metadata)
        environment = kwargs.pop("environment", self.environment)
        implementation = kwargs.pop("implementation", self.implementation)
        framework = kwargs.pop("framework", self.framework)
        algorithm = kwargs.pop("algorithm", self.algorithm)
        tag = kwargs.pop("tag", self.tag)
        model_type = kwargs.pop("model_type", self.model_type)
        model_name = kwargs.pop("model_name", "")

        return {
            'metadata': metadata,
            'environment': environment,
            'implementation': implementation,
            'framework': framework,
            'algorithm': algorithm,
            'tag': tag,
            'model_type': model_type,
            'model_name': model_name
        }

    def deploy_new_version(self, model_id: str, model_class: str, model_files: List[str], requirements_file: str, **kwargs):
        files = [*model_files, requirements_file]

        validate_files(files)
        validate_model_class(model_class, model_files)

        parameters = self.retrieve_optional_parameters(**kwargs)

        parameters['model_class'] = model_class
        parameters['model_files'] = model_files
        parameters['requirements_file'] = requirements_file

        self.model.get(model_id)

        model_version = self.model.create_version(
            **parameters
        )

        self.__deploy(files, model_version)

        return self.model, model_version

    def deploy(self, model_class: str, model_files: List[str], requirements_file: str, **kwargs) -> Tuple[Model, ModelVersion]:

        files = [*model_files, requirements_file]

        validate_files(files)
        validate_model_class(model_class, model_files)

        parameters = self.retrieve_optional_parameters(**kwargs)
        parameters['model_class'] = model_class
        parameters['model_files'] = model_files
        parameters['requirements_file'] = requirements_file

        if self.model_id == None:
            self.model.create(name=parameters["model_name"], **kwargs)
        else:
            self.model.get(self.model_id)

        if self.model_version_id == None:
            model_version = self.model.create_version(
                **parameters
            )
        else:
            model_version = self.model.get_version(self.model_version_id)
            model_version.update(**parameters)

        self.__deploy(files, model_version)

        return self.model, model_version

    def __deploy(self, files: List[str], model_version: ModelVersion):
        package = prepare_package(files)

        model_version.upload_package(package_url=package)

        model_version.deploy()

        clean_tmp()

        click.secho('########################################', fg='yellow')
        click.secho(f"### MODEL ID: {self.model.model_id} ###", fg='yellow')
        click.secho('########################################', fg='yellow')

    def predict(self, inputs: List):
        return self.model.predict(inputs=inputs)

    def health(self):
        return self.model.health()
