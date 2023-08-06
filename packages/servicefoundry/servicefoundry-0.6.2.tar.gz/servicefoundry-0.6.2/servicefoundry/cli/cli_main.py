import logging
import os

import rich_click as click

from servicefoundry import logger
from servicefoundry.cli.commands import (
    deploy_v2_command,
    get_build_command,
    get_create_command,
    get_delete_command,
    get_get_command,
    get_list_command,
    get_login_command,
    get_logout_command,
    get_logs_command,
    get_set_command,
)
from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import GROUP_CLS
from servicefoundry.cli.util import setup_rich_click
from servicefoundry.version import __version__


def _add_internal_commands(cli):
    from servicefoundry.cli.commands.infra_bootstrap import get_infra_command

    cli.add_command(get_infra_command())


def create_service_foundry_cli():
    """Generates CLI by combining all subcommands into a main CLI and returns in

    Returns:
        function: main CLI functions will all added sub-commands
    """
    _cli = service_foundry_cli
    _cli.add_command(get_login_command())
    # _cli.add_command(get_get_command())
    _cli.add_command(get_list_command())
    # _cli.add_command(get_delete_command())
    # _cli.add_command(get_create_command())
    _cli.add_command(get_logout_command())
    _cli.add_command(get_set_command())
    _cli.add_command(get_build_command())
    _cli.add_command(deploy_v2_command)
    _cli.add_command(get_logs_command())
    if os.getenv("SFY_INTERNAL"):
        _add_internal_commands(_cli)
    return _cli


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(
    cls=GROUP_CLS, context_settings=CONTEXT_SETTINGS, invoke_without_command=True
)
@click.option("--json", is_flag=True)
@click.option(
    "--debug", is_flag=True, default=False, help="Enable debug logger with the command"
)
@click.version_option(__version__)
@click.pass_context
def service_foundry_cli(ctx, json, debug):
    """
    Servicefoundry provides an easy way to deploy your code as a web service.
    \b

    To start, login to your Truefoundry account with `sfy login`

    \b
    Once logged in, start a new service with `sfy init`
    """
    setup_rich_click()
    # TODO (chiragjn): Change this to -o json|yaml|table|pager
    CliConfig.set("json", json)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    logger.add_cli_handler(level=logging.DEBUG if debug else logging.INFO)
