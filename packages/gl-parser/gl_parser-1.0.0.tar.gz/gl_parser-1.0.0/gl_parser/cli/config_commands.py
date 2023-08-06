import logging
import sys
from pathlib import Path
from typing import Optional

import click

from gl_parser import ConfigurationManager, CONFIGURATION_MANAGER
from gl_parser.enums import ExitCode
from gl_parser.exceptions import GLParserException

logger = logging.getLogger(__name__)


@click.command()
@click.argument('sub_command', required=False)
@click.option('--overwrite', is_flag=True, default=False, help="Overwrite the configuration file.")
def config(sub_command, overwrite):
    """Configure the application. Sub commands:

    SHOW: shows current configuration.
    DELETE: deletes current configuration."""
    if sub_command is None:
        click.echo('Configuration')
        do_configuration(overwrite)
    elif sub_command == 'show':
        do_show()
    else:
        click.echo(f'sub command {sub_command}')


def do_configuration(overwrite: bool, configuration_manager: Optional[ConfigurationManager] = None):
    if configuration_manager is None:
        configuration_manager = CONFIGURATION_MANAGER
    if configuration_manager.config_file.exists() and not overwrite:
        click.secho('Configuration file already exists. Run with --overwrite flag.', fg='red')
        sys.exit(ExitCode.CANNOT_OVERWRITE)
    configuration = CONFIGURATION_MANAGER.get_current()
    try:
        output_folder_prompt = 'Type the default output folder'
        output_folder_name = click.prompt(output_folder_prompt, default=configuration['application']['output_folder'])
        output_folder = Path(output_folder_name)
        if not output_folder.exists():
            message = f'The supplied folder does not exist {output_folder_name} please create it.'
            click.secho(message, fg='red')
            logger.warning(message)
            sys.exit(ExitCode.INVALID_CONFIGURATION)
        if not output_folder.is_dir():
            message = f'The supplied folder is not a folder {output_folder_name}.'
            click.secho(message, fg='red')
            logger.warning(message)
            sys.exit(ExitCode.INVALID_CONFIGURATION)
        configuration['application']['output_folder'] = str(output_folder.resolve())
        backup_file = configuration_manager.backup()
        logger.debug(f'Backed up configuration to {backup_file} before writing.')

        configuration_manager.write_configuration(configuration, overwrite=overwrite)

    except KeyError as e:
        error_message = f'Configuration error key not found. Error: {e}'
        logger.debug(error_message)
        raise GLParserException(error_message)


def do_show(configuration_manager: Optional[ConfigurationManager] = None):
    if configuration_manager is None:
        configuration_manager = CONFIGURATION_MANAGER
    with open(configuration_manager.config_file, 'r') as f:
        text = f.read()
    click.echo(text)
