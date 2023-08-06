from setuptools import setup, find_packages

long_description = open('./README.md')

setup(
    name='Paramo',
    version='1.0.0',
    url='https://github.com/ZSendokame/Paramo',
    license='MIT license',
    author='ZSendokame',
    description='Better HTTP parameters.',
    long_description=long_description.read(),
    long_description_content_type='text/markdown',
    packages=(find_packages(include=['paramo'])),

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
    ]
)
