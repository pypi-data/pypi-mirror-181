# Manuel Eggimann <meggimann@iis.ee.ethz.ch>
#
# Copyright (C) 2021-2022 ETH Zürich
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import time
import traceback
from pathlib import Path

from mako.template import Template

import padrick.Generators.CLIGeneratorCommands
import click
import click_completion
import click_spinner
import click_log
import json

from padrick.Generators.FuseSoCGenerator.FuseSoCGenerator import generate_core
from padrick.Generators.GeneratorSettings import RTLTemplates
from padrick.Generators.RTLGenerator.RTLGenerator import generate_rtl
from padrick.Generators import CLIGeneratorCommands
from padrick.ConfigParser import parse_config
from padrick.Model.Padframe import Padframe
from padrick.Model.PadSignal import Signal
from padrick.Model.SignalExpressionType import SignalExpressionType

logger = logging.getLogger("padrick")
click_log.basic_config(logger)

click_completion.init()
_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=_CONTEXT_SETTINGS)
@click.version_option()
def cli():
    """
    Generate padframes for SoC
    """

@cli.command()
@click.option('--append/--overwrite', help="Append the completion code to the file", default=None)
@click.option('-i', '--case-insensitive/--no-case-insensitive', help="Case insensitive completion")
@click.argument('shell', required=False, type=click_completion.DocumentedChoice(click_completion.core.shells))
@click.argument('path', required=False)
def install_completions(append, case_insensitive, shell, path):
    """Install the command line tool's bash completion for your shell

    If you don't provide any additional arguments this command tries to detect your current shell in use and appends the relevant settings to your .bashrc, .zshrc etc."""
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    shell, path = click_completion.core.install(shell=shell, path=path, append=append, extra_env=extra_env)
    click.echo('%s completion installed in %s' % (shell, path))

@cli.command()
@click.argument('file', type=click.Path(dir_okay=False, file_okay=True, exists=True, readable=True))
@click_log.simple_verbosity_option(logger)
def validate(file):
    """ Parse and validate the given config file
    """
    with click_spinner.spinner():
        model = parse_config(Padframe, Path(file))
        if model != None:
            click.echo(f"Successfully parsed configuration file.")
        else:
            click.echo(f"Error while parsing configuration file {file}")

@cli.command()
@click.argument('file', type=click.Path(dir_okay=False, file_okay=True, exists=True, readable=True))
@click_log.simple_verbosity_option(logger)
def config(file):
    """ Print the parsed padframe configuration file """
    with click_spinner.spinner():
        model = parse_config(Padframe, Path(file))
    if model != None:
        class ModelEncoder(json.JSONEncoder):
            def default(self, o):
                return str(o)
            def sanitize(self, o):
                if isinstance(o, list):
                    return [self.sanitize(v) for v in o]
                if isinstance(o, tuple):
                    return tuple([self.sanitize(v) for v in o])
                elif isinstance(o, dict):
                    return {self.sanitize(key): self.sanitize(v) for key, v in o.items()}
                elif isinstance(o, Template):
                    return o.source
                elif isinstance(o, SignalExpressionType):
                    if o.is_empty:
                        return None
                    else:
                        return o.expression
                elif isinstance(o, Signal):
                    return o.name
                else:
                    return o
            def encode(self, o):
                return super().encode(self.sanitize(o))
        click.echo(json.dumps(model.dict(), cls=ModelEncoder, indent=4))
    else:
        click.echo(f"Error while parsing configuration file {file}")

@cli.command()
@click.argument('config_file', type=click.Path(dir_okay=False, file_okay=True, exists=True, readable=True))
def fusesoc_gen(config_file):
    """Generator invocation for FuseSoC.

    Parses the supplied config_file command and generates RTL + Core files in the current direcotry.
    Check the documentation for more information about available FuseSoC Generator parameters.
    """
    click.echo("Padrick started in FuseSoC generator mode.")
    generate_core(Path(config_file))
    click.echo("Finished core generation")

# Register first level subcommand
cli.add_command(padrick.Generators.CLIGeneratorCommands.generate)

# For debugging purposes only
if __name__ == '__main__':
    #cli(['rosetta', '-o' 'test.avc', 'write-mem', '0x1c008080=0xdeadbeef'])
    # while True:
        cli(['generate', 'template-customization'])
        cli(['generate', '-s', 'padrick_gen_settings.yml', 'rtl'])
        config_file = '../../examples/siracusa_pads.yml'
        output = '/home/meggiman/garbage/test_padrick_siracusa'
        try:
            padframe = parse_config(Padframe, Path(config_file))
            if padframe:
                generate_rtl(RTLTemplates(), padframe, Path(output), header_text="")
                print("Generated RTL")
        except Exception as e:
            traceback.print_exc()
            pass
        # time.sleep(5)

    # cli(['generate', 'driver',  '-v' 'INFO', '-o', '/home/meggiman/garbage/test_padrick/driver',
    #          '../../examples/sample_padframe.yaml'])

    #cli(['config', '../../examples/kraken_padframe.yml'])