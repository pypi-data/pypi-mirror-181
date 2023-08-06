import os
import platform
import shutil
import stat
import tarfile
import urllib.request
import zipfile
from enum import Enum

from servicefoundry.lib.const import HELM_VERSION, TERRAFORM_VERSION, TERRAGRUNT_VERSION


class BinaryName(Enum):
    TERRAFORM = "terraform"
    TERRAGRUNT = "terragrunt"
    HELM = "helm"


class OsType(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    DARWIN = "darwin"


class BinaryDependencies:
    def __init__(self):
        # folder containing all the binaries
        self.dir = os.path.join(os.path.expanduser("~"), ".truefoundry", "bin")
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.ostype = platform.system().lower()
        self.processor = platform.machine().lower()
        self.urls_map = {
            BinaryName.TERRAFORM: {
                OsType.WINDOWS.value: f"https://releases.hashicorp.com/terraform/{TERRAFORM_VERSION}/terraform_{TERRAFORM_VERSION}_windows_{self.processor}.zip",
                OsType.LINUX.value: f"https://releases.hashicorp.com/terraform/{TERRAFORM_VERSION}/terraform_{TERRAFORM_VERSION}_linux_{self.processor}.zip",
                OsType.DARWIN.value: f"https://releases.hashicorp.com/terraform/{TERRAFORM_VERSION}/terraform_{TERRAFORM_VERSION}_darwin_{self.processor}.zip",
            },
            BinaryName.TERRAGRUNT: {
                OsType.WINDOWS.value: f"https://github.com/gruntwork-io/terragrunt/releases/download/v{TERRAGRUNT_VERSION}/terragrunt_windows_{self.processor}.exe",
                OsType.LINUX.value: f"https://github.com/gruntwork-io/terragrunt/releases/download/v{TERRAGRUNT_VERSION}/terragrunt_linux_{self.processor}",
                OsType.DARWIN.value: f"https://github.com/gruntwork-io/terragrunt/releases/download/v{TERRAGRUNT_VERSION}/terragrunt_darwin_{self.processor}",
            },
            BinaryName.HELM: {
                OsType.WINDOWS.value: f"https://get.helm.sh/helm-v{HELM_VERSION}-windows-{self.processor}.tar.gz",
                OsType.LINUX.value: f"https://get.helm.sh/helm-v{HELM_VERSION}-linux-{self.processor}.tar.gz",
                OsType.DARWIN.value: f"https://get.helm.sh/helm-v{HELM_VERSION}-darwin-{self.processor}.tar.gz",
            },
        }

    def which(self, binary: BinaryName = None):
        if binary.value == BinaryName.TERRAFORM.value:
            return self.__get_terraform_path()
        elif binary.value == BinaryName.TERRAGRUNT.value:
            return self.__get_terragrunt_path()
        elif binary.value == BinaryName.HELM.value:
            return self.__get_helm_path()
        else:
            raise Exception("Invalid binary name")

    # Funtion to add executable permission to the binary
    def __add_executable_permission(self, path_to_executable):
        state = os.stat(path_to_executable)
        os.chmod(path_to_executable, state.st_mode | stat.S_IEXEC)

    def __get_terraform_path(self):
        terraform_path = os.path.join(self.dir, BinaryName.TERRAFORM.value)
        # check if terraform already exists
        if os.path.exists(terraform_path):
            return terraform_path

        # get url to download binary, based on os type and processor type
        url = self.urls_map[BinaryName.TERRAFORM][self.ostype]
        file_name = os.path.join(self.dir, "terraform.zip")
        urllib.request.urlretrieve(url, file_name)

        # extract the dowloaded zip and move the binary to destination
        with zipfile.ZipFile(file_name, "r") as zip_file:
            zip_file.extractall(self.dir)
            # clean unwanted files
            os.remove(file_name)
        self.__add_executable_permission(terraform_path)

        return terraform_path

    def __get_terragrunt_path(self):
        terragrunt_path = os.path.join(self.dir, BinaryName.TERRAGRUNT.value)
        if os.path.exists(terragrunt_path):
            return terragrunt_path

        url = self.urls_map[BinaryName.TERRAGRUNT][self.ostype]
        urllib.request.urlretrieve(
            url, os.path.join(self.dir, BinaryName.TERRAGRUNT.value)
        )

        self.__add_executable_permission(terragrunt_path)
        return terragrunt_path

    def __get_helm_path(self):
        helm_path = os.path.join(self.dir, BinaryName.HELM.value)
        if os.path.exists(helm_path):
            return helm_path

        url = self.urls_map[BinaryName.HELM][self.ostype]
        file_name = os.path.join(self.dir, "helm.tar.gz")
        urllib.request.urlretrieve(url, file_name)

        with tarfile.open(file_name, "r:gz") as tar_file:
            dir_name = os.path.join(self.dir, tar_file.getnames()[0])
            tar_file.extractall(self.dir)
            shutil.move(
                os.path.join(dir_name, BinaryName.HELM.value),
                os.path.join(self.dir, BinaryName.HELM.value),
            )
            shutil.rmtree(dir_name)
            os.remove(file_name)
        self.__add_executable_permission(helm_path)
        return helm_path
