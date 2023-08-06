import json
import os

from cookiecutter.main import cookiecutter


class CookieCutter:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def updateProvisioningConfig(self, provisioning_config):
        with open(
            os.path.join(self.template_path, "cookiecutter.json"), "r+"
        ) as cookiecutter_config_file:
            cookiecutter_config = json.load(cookiecutter_config_file)
            cookiecutter_config["provisioning"] = provisioning_config
            cookiecutter_config_file.seek(0)
            cookiecutter_config_file.write(json.dumps(cookiecutter_config, indent=2))
            cookiecutter_config_file.truncate()

    def run(self, destination_dir):
        current_dir = os.getcwd()
        os.chdir(os.path.join(destination_dir))
        generated_repo_path = cookiecutter(self.template_path, no_input=True)
        os.chdir(current_dir)
        return generated_repo_path
