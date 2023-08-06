import versioneer
from setuptools import find_namespace_packages, setup

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='drb',
    packages=find_namespace_packages(include=['drb.*'], exclude=['tests']),
    description='Data Request Broker',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/drb',
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    use_scm_version=True,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    package_data={
        'drb.factory': ['it_schema.yml']
    },
    data_files=[('.', ['requirements.txt'])],
    entry_points={
        'console_scripts': [
            'cortex-validator=drb.core.cortex_validator:main',
            'wallet=drb.utils.keyring:keyring'
        ],
        'drb.signature': [
            'name = drb.signatures.core:NameSignature',
            'namespace = drb.signatures.core:NamespaceSignature',
            'path = drb.signatures.core:PathSignature',
            'attributes = drb.signatures.core:AttributesSignature',
            'children = drb.signatures.core:ChildrenSignature',
            'python = drb.signatures.core:PythonSignature',
        ]
    },
    project_urls={
        'Documentation': 'https://drb-python.gitlab.io/drb',
        'Source': 'https://gitlab.com/drb-python/drb',
    }
)
