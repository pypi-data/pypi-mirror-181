import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cakework',
    version='0.0.8',
    author='Jessie Young',
    author_email='jessie@sahale.io',
    description='Python SDK for Cakework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/usecakework/sdk-python',
    project_urls = {
        "Bug Tracker": "https://github.com/usecakework/sdk-python/issues"
    },
    license='MIT',
    packages=['cakework'],
    install_requires=[],
)
