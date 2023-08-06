from skbuild import setup

setup(
    name='ws2223-group7-hanabi-learning-environment-alexb',
    version='0.0.1',    
    description='ws2223-group7 Learning environment for the game of hanabi for alexb.',
    long_description='ws2223-group7 Learning environment for the game of hanabi for alexb.',
    long_description_content_type="text/markdown",
    author='ws2223-group7/hanabi-learning-environment',
    packages=['hanabi_learning_environment', 'hanabi_learning_environment.agents', 'bad'],
    install_requires=['cffi'],
    python_requires=">=3.6",
    classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: POSIX :: Linux",
    ]    
)
