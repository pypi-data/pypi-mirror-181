import sys
import tomli
import os
import argparse
from dataclasses import dataclass
import yaml


@dataclass
class Deploy:
    command: str
    branch: str
    service: str
    stack_name: str
    config: dict
    docker_dir: str = ""
    stack_file: str = "stack.yml"


    def get_root_path(self):
        return f'{os.getcwd()}/{self.config["docker_dir"]}/{self.config["env"]}'

    def get_dockerfile_path(self) -> str:
        root_path: str = self.get_root_path()
        return f'${root_path}/{self.service}/Dockerfile'

    def get_stack_path(self) -> str:
        root_path: str = self.get_root_path()
        return f'{root_path}/stack.yml'

    def get_image_tag(self):
        stack_file: str = self.get_stack_path()
        with open(stack_file, "r") as stream:
            try:
                stack_data = yaml.safe_load(stream)
                return stack_data.get('services').get(self.service).get('image')
            except Exception as e:
                raise e

    def run_build(self):
        dockerfile_path: str = self.get_dockerfile_path()
        service_image_tag: str = self.get_image_tag()
        os.system(f"docker build -f {dockerfile_path} -t {service_image_tag} .")

    def run_deploy(self):
        stack_path: str = self.get_stack_path()
        os.system(f"docker stack deploy -c {stack_path} {self.stack_name}")

    def run(self):
        if self.command == "build":
            self.run_build()
        if self.command == "deploy":
            self.run_deploy()


def get_config():
    custom_dir_path = os.getcwd()
    if os.path.exists(f'{custom_dir_path}/.config.toml'):
        with open(f'{custom_dir_path}/.config.toml', mode="rb") as fp:
            config = tomli.load(fp)
    else:
        default_dir_path: str = os.path.dirname(os.path.realpath(__file__))
        with open(f"{default_dir_path}/config.toml", mode="rb") as fp:
            config = tomli.load(fp)
    return config


def parse_cli_arguments():
    parser = argparse.ArgumentParser(
        description="Install a stack file on docker swarm."
    )
    parser.add_argument(
        "--command", type=str, help="wich docker command execute [build, deploy]"
    )
    parser.add_argument(
        "--branch",
        type=str,
        dest="branch",
        help="the branch to clone inside Dockerfile",
    )
    parser.add_argument(
        "--service",
        type=str,
        dest="service",
        help="the stack service to build image",
    )
    parser.add_argument(
        "--stack",
        type=str,
        dest="stack_name",
        help="the name to use as prefix for docker services.",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_cli_arguments()
    config = get_config()
    deploy = Deploy(args.command, args.branch, args.service, args.stack_name, config)
    deploy.run()


if __name__ == "__main__":
    main()
