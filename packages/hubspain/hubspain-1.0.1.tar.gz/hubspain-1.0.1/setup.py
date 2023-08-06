from setuptools import setup

readme = open("./README.md", "r")

setup(
    name='hubspain',
    packages=['hubspain'],  # this must be the same as the name above
    version='1.0.1',
    description='Esta es la descripcion de mi paquete',
    long_description=readme.read(), # this is the readme file
    long_description_content_type='text/markdown',
    author='flowese',
    author_email='flowese@gmail.com',
    # use the URL to the github repo
    url='https://github.com/flowese/hubspain-tools',
    download_url='https://github.com/flowese/hubspain-tools/tarball/1.0.0',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True,
    # Otros argumentos del setup
    install_requires=[
        "aiohttp==3.8.3",
        "Pillow==9.3.0",
        "requests==2.28.1",
    ],
)