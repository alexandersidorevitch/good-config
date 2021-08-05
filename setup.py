import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='good_config',
    version='0.1',
    scripts=['casters.py', 'config.py', 'exceptions.py', 'field.py', 'providers.py'],
    author='Alexander Sidorevich',
    author_email='alexandersidorevitch@yandex.by',
    description='A Docker and AWS utility package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alexandersidorevitch/good-config',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
