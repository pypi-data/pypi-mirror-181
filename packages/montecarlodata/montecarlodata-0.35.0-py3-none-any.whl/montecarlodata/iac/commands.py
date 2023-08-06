import click
import click_config_file

from montecarlodata import settings
from montecarlodata.iac.mc_config_service import MonteCarloConfigService
from montecarlodata.monitors.monitor_service import MonitorService


@click.group(help='Manage monitors.')
def monitors():
    """
    Group for any monitor related subcommands
    """
    pass

@monitors.command(help='Compile monitor configuration.')
@click.option('--project-dir', required=False, help='Base directory of MC project (where montecarlo.yml is located). By default, this is set to the current working directory')
@click.pass_obj
def compile(ctx, project_dir):
    MonteCarloConfigService(config=ctx['config'], project_dir=project_dir).compile()

@monitors.command(help='Compile and apply monitor configuration.')
@click.option('--project-dir', required=False, help='Base directory of MC project (where montecarlo.yml is located). By default, this is set to the current working directory')
@click.option('--namespace', required=True, help='Namespace of monitors configuration.')
@click.option('--dry-run', required=False, default=False, show_default=True, is_flag=True, help='Dry run (just shows planned changes but doesn\'t apply them.')
@click.pass_obj
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def apply(ctx, project_dir, namespace, dry_run):
    MonteCarloConfigService(config=ctx['config'], project_dir=project_dir).apply(namespace, dry_run=dry_run)

@monitors.command(help='Delete monitor configuration.')
@click.option('--project-dir', required=False, help='Base directory of MC project (where montecarlo.yml is located). By default, this is set to the current working directory')
@click.option('--namespace', required=True, help='Namespace of monitors configuration.')
@click.option('--dry-run', required=False, default=False, show_default=True, is_flag=True, help='Dry run (just shows planned changes but doesn\'t apply them.')
@click.pass_obj
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def delete(ctx, project_dir, namespace, dry_run):
    MonteCarloConfigService(config=ctx['config'], project_dir=project_dir).delete(namespace, dry_run=dry_run)

@monitors.command(name='list', help='List monitors ordered by update recency.')
@click.option('--limit', required=False, default=100, type=click.INT, show_default=True, help='Max number of monitors to list.')
@click.option(
    '--monitor-type',
    required=False,
    type=click.Choice(MonitorService.MONITOR_TYPES, case_sensitive=False),
    help='List monitors with monitor_type'
)
@click.option(
    '--namespace',
    required=False,
    help='List only monitors in this namespace'
)
@click.pass_obj
def list_monitors(ctx, monitor_type, limit, namespace):
    monitor_types = None
    namespaces = [namespace] if namespace else None
    if monitor_type:
        if monitor_type == MonitorService.PSEUDO_MONITOR_TYPE_CB_COMPATIBLE:
            monitor_type = MonitorService.MONITOR_TYPE_CUSTOM_SQL
        monitor_types = [monitor_type]
    MonitorService().list_monitors(limit, namespaces, monitor_types)

@monitors.command(name='namespaces', help='List all namespaces.')
@click.option('--limit', required=False, default=100, type=click.INT, show_default=True,
              help='Max number of namespaces to list.')
@click.pass_obj
def list_namespaces(ctx, limit):
    MonteCarloConfigService(config=ctx['config']).list_namespaces(limit)
