# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pencilctl-lite']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'tomli']

setup_kwargs = {
    'name': 'pencilctl-lite',
    'version': '0.0.11',
    'description': 'A simple package to help deploy docker swarm stack.',
    'long_description': '# pencilctl_lite\n\nRepositório contendo o script pencilctl_lite, responsável por fazer deploy de projetos que utilizem uma estrutura de docker stack, mas que não serão executados no cluster principal da Pencil.\n\n## Quick Start\n\nPara utilizar este script, existem algumas pré-requisitos:\n\n1. Um cluster swarm tem que existir na máquina em que ele será executado;\n2. O projeto que será alvo do deploy deve possuir uma pasta `docker/production`, contendo os arquivos Dockerfile (caso as stacks exigam imagens customizadas), e os arquivos de stack, que serão utilizados para realizar o deploy do projeto.\n3. O diretório  `docker/production`, deve ter a seguinte estrutura:\n\n![estrutura ](./estrutura.png)\n\n- **xpto**: Diretório que centraliza todos os arquivos de uma stack. Um projeto pode ter mais de uma stack, por exemplo, uma stack para fazer deploy do servidor, e outra para um http proxy ou um redis. O pencilctl _lite permite fazer deploy de multiplas stacks. Diretório obrigatório;\n- **xpto/stacks**: Diretório contendo os arquivos de stack do projeto.  Diretório obrigatório;\n- **xpto/nginx_confs**: Diretório contendo arquivos de configuração do nginx. Diretório optativo;\n- **xpto/server**: Diretório contendo o Dockerfile do serviço chamado server, declarado no arquivo de stack. Diretório optativo;\n- **xpto/db**: Diretório contendo o Dockerfile do serviço chamado db, declarado no arquivo de stack. Diretório optativo;\n- **xpto/nginx**: Diretório contendo o Dockerfile do serviço chamado nginx, declarado no arquivo de stack Diretório optativo;\n\nEssa estrutura deve existir **no repositório do projeto** que será alvo do deploy. O papel do script é apenas acessar esse diretório e automatizar os processos de build e deploy. Essa estrutura também padroniza o nome/tag das imagens que são construidas via `./pencilctl_lite build`.\n\nSupondo a stack xpto, o comando para buildar a imagem do server seria:\n\n    ./pencilctl_lite.sh build --docker_path=/home/user/xpto/docker --service=server --stack=xpto\n\nEste comando geraria a imagem `127.0.0.1:5000/xpto_server:stable-prod`.\n\nO comando para fazer deploy da stack:\n\n    ./pencilctl_lite.sh deploy --docker_path=/home/user/xpto/docker --stack=xpto\n\nEste comando geraria a stack `xpto_prod`.\n\nPara saber quais comandos o script possui e quais argumentos ele recebe, basta executar:\n\n    ./pencilctl_lite.sh help\n',
    'author': 'David Carlos',
    'author_email': 'ddavidcarlos1392@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/pencillabs/infraestructure/pencilctl_lite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
