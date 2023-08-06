from setuptools import setup, find_packages

setup(
    name='pystego',
    version='0.0.21',
    description='A Python program that allows you to save secret messages in images',
    author='Miquel Muntaner',
    author_email='miquemuntanerweb@gmail.com',
    url='https://github.com/MiquelMuntaner/pystego',
    py_modules=['pystego'],
    package_dir={'': 'src'},
    packages=find_packages(include=('colors', 'decoding', 'encoding', 'encryption_tools', 'interface', 'translation_tools')),
    install_requires=['bullet', 'click', 'Pillow', 'pycryptodomex', 'typer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License"
    ]
)