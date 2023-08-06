import rich_click as click

from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.lib.infra.infra_bootstrap import Infra


@click.group(
    name="infra",
    cls=GROUP_CLS,
)
def infra():
    pass


@click.command(
    name="bootstrap",
    cls=COMMAND_CLS,
    help="Bootstrap truefoundry platform on an existing Kubernetes cluster",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
)
@click.option(
    "--bootstrap-only",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default=None,
    help="path to infra bootstrap config file",
    show_default=False,
)
def infra_bootstrap(dry_run: bool, bootstrap_only: str):
    infra_object = Infra(dry_run=dry_run)
    if bootstrap_only:
        infra_object.bootstrap(infra_config_file_path=bootstrap_only)
    else:
        infra_object.provision()


def get_infra_command():
    infra.add_command(infra_bootstrap)
    return infra
