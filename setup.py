from setuptools import setup, find_packages

setup(
    name='caixa.gsc',
    version='0.2',
    description='Biblioteca de comunicação com os webservices de Gerenciamento de Serviços da Caixa Econômica',
    author='Clayton A. Alves',
    author_email='clayton.aa@gmail.com',
    url='https://github.com/claytonaalves/caixa.gsc',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests>=2.19.1',
        'zeep>=3.1.0'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
