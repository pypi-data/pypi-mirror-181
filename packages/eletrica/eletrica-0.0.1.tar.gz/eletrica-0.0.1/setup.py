from setuptools import setup

setup(
    name='eletrica',
    version='0.0.1',
    description='Módulo para auxiliar no cálculo de circuitos elétricos no domínio da frequência, através da implementação de classes e funções para tratamento de grandezas nos formatos retangular e polar, conforme os padrões utilizados em estudos de Engenharia Elétrica.',
    author='Allan M. Cavalari',
    url='https://github.com/allancavalari/eletrica',    
    packages=['eletrica'],
    install_requires=[
        'numpy',
    ],
)