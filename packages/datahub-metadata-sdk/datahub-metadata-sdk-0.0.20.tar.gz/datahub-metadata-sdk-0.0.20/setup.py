import os
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read().strip()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths
extra_files = package_files('metadata/client/resources')

setup(
    name='datahub-metadata-sdk',
    version='0.0.20',
    description='Datahub metastore concept Simplified.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="DP Technology",
    packages=find_packages(exclude=['tests', 'examples']),
    package_data={'': extra_files},
    python_requires='>=3.8',
    install_requires=[
        "requests",
        "backoff",
        "acryl-datahub[datahub-rest]",
        "validators",
        "python-dateutil",
        "pyjwt",
        "lbg>=1.2.9",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "metadata = metadata.cli.commands.metadata:main [cli]",
        ]
    },
    extras_require={
        "cli": [
            'sh',
            'jsonpath_ng',
            'pandas',
            'coloredlogs',
            'streamlit',
        ]
    },
)
