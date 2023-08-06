from setuptools import setup

# General Setup
PIP_NAME = 'maci'
VERSION = '0.1.0'
CODE_AUTHOR = 'aaronater10'
AUTHOR_EMAIL = 'dev_admin@dunnts.com'
PROJECT_URL = f'https://github.com/aaronater10/{PIP_NAME}'
MODULES_INSTALLED = [PIP_NAME]

# Descriptions
DESCRIPTION = 'maci'
with open('.\\README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

# Main Setup Params
setup(
    name=PIP_NAME,
    version=VERSION,
    url=PROJECT_URL,
    author=CODE_AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=MODULES_INSTALLED,
    packages=[PIP_NAME],
    package_dir={PIP_NAME: PIP_NAME},
    include_package_data=True,
    install_requires=[""],
    keywords=['python', 'py', 'bin', 'file', 'runtime', 'env', 'environment', 'universal', 'win', 'windows', 'windows 10', 'mac', 'osx', 'macintosh', 'linux', 'debian', 'redhat', 'ubuntu', 'centos', 'import'],
    license = 'MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ]
)
