import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='elnasmartmeter',
    version='1.1.0',
    author='Mikael Schultz',
    author_email='bitcanon@pm.me',
    description='A simple library for the E.ON Elna API written in Python 3.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bitcanon/elnasmartmeter',
    packages=setuptools.find_packages(),
    install_requires=['requests', 'python-dateutil'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
