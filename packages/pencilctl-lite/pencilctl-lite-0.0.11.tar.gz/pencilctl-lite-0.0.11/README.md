# pencilctl_lite

Repositório contendo o script pencilctl_lite, responsável por fazer deploy de projetos que utilizem uma estrutura de docker stack, mas que não serão executados no cluster principal da Pencil.

## Quick Start

Para utilizar este script, existem algumas pré-requisitos:

1. Um cluster swarm tem que existir na máquina em que ele será executado;
2. O projeto que será alvo do deploy deve possuir uma pasta `docker/production`, contendo os arquivos Dockerfile (caso as stacks exigam imagens customizadas), e os arquivos de stack, que serão utilizados para realizar o deploy do projeto.
3. O diretório  `docker/production`, deve ter a seguinte estrutura:

![estrutura ](./estrutura.png)

- **xpto**: Diretório que centraliza todos os arquivos de uma stack. Um projeto pode ter mais de uma stack, por exemplo, uma stack para fazer deploy do servidor, e outra para um http proxy ou um redis. O pencilctl _lite permite fazer deploy de multiplas stacks. Diretório obrigatório;
- **xpto/stacks**: Diretório contendo os arquivos de stack do projeto.  Diretório obrigatório;
- **xpto/nginx_confs**: Diretório contendo arquivos de configuração do nginx. Diretório optativo;
- **xpto/server**: Diretório contendo o Dockerfile do serviço chamado server, declarado no arquivo de stack. Diretório optativo;
- **xpto/db**: Diretório contendo o Dockerfile do serviço chamado db, declarado no arquivo de stack. Diretório optativo;
- **xpto/nginx**: Diretório contendo o Dockerfile do serviço chamado nginx, declarado no arquivo de stack Diretório optativo;

Essa estrutura deve existir **no repositório do projeto** que será alvo do deploy. O papel do script é apenas acessar esse diretório e automatizar os processos de build e deploy. Essa estrutura também padroniza o nome/tag das imagens que são construidas via `./pencilctl_lite build`.

Supondo a stack xpto, o comando para buildar a imagem do server seria:

    ./pencilctl_lite.sh build --docker_path=/home/user/xpto/docker --service=server --stack=xpto

Este comando geraria a imagem `127.0.0.1:5000/xpto_server:stable-prod`.

O comando para fazer deploy da stack:

    ./pencilctl_lite.sh deploy --docker_path=/home/user/xpto/docker --stack=xpto

Este comando geraria a stack `xpto_prod`.

Para saber quais comandos o script possui e quais argumentos ele recebe, basta executar:

    ./pencilctl_lite.sh help
