import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sahale',
    version='0.0.3',
    author='Jessie Young',
    author_email='jessie@sahale.io',
    description='Python SDK for Sahale',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sahaleio/sdk-python',
    project_urls = {
        "Bug Tracker": "https://github.com/sahaleio/sdk-python/issues"
    },
    license='MIT',
    packages=['sahale'],
    install_requires=[],
)
