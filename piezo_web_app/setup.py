from PiezoWebApp import version
from setuptools import setup, find_packages

setup(
    # Application name:
    name='PiezoWebApp',

    # Version number (initial):
    version=version.__version__,

    # Application author details:
    author="Piezo team",
    author_email="some@email",

    # Packages
    packages=find_packages(),
    package_data={
        # Include the configuration file in the resulting wheel
        '': ['example_configuration.ini', 'example_bucket_settings.ini'],
    },

    description="Web app for submitting Spark jobs to Kubernetes cluster.",

    # Dependent packages (distributions)
    install_requires=[
        "requests"
    ],

    # entry points
    entry_points={
        'console_scripts': [
            'piezo_server = PiezoWebApp.run_piezo:launch'
        ]
    },
)
