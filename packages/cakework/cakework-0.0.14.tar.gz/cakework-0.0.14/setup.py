import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cakework',
    version='0.0.14',
    author='Jessie Young',
    author_email='jessie@cakework.com',
    description='Python SDK for Cakework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/usecakework/sdk-python',
    project_urls = {
        "Bug Tracker": "https://github.com/usecakework/sdk-python/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['grpcio', 'protobuf'],
)
