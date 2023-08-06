from setuptools import setup,find_packages

from pathlib import Path

setup(
    name='Pro_Car_Automation',
    version=1.0,
    description='este pacote irá fornecer ferramentas de automação para veículos',
    long_description=Path('README.md').read_text(),
    author='Estevao Ramos',
    author_email='estevao.sr@live.com',
    keywords=['carro','automation','processamento'],
    packages=find_packages()
)

#após esta parte digitar no terminal o seguinte comando:
# pip install setuptools twine para instalar os pacotes setuptools e twine
#após a instalação digitar o comando: python .\setup.py sdist
#agora queremos enviar o arquivo .tar.gz para o pypi.org
#uso o comando: twine upload --repository-url https://upload.pypi.org/legacy/ dist/*