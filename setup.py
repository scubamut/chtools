from setuptools import setup, find_packages

setup(
    name='chtools',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Dave Gilbert',
    author_email='scubamut@gmail.com',
    description='A package to interact with the UK Companies House API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://pypi.python.org/pypi/chtools/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: ubuntu',
    ],
    python_requires='>=3.10'
)

