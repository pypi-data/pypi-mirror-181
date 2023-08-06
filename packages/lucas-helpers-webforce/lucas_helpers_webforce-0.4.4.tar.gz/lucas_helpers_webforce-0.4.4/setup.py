from setuptools import setup

with open('README.md', 'r') as puntero:
    long_description = puntero.read()


setup(
    name='lucas_helpers_webforce',
    packages=['lucas_helpers_webforce'],  # this must be the same as the name above
    version='0.4.4',
    description='description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Webforce',
    author_email='',
    # use the URL to the github repo
    url='',
    download_url='',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
)