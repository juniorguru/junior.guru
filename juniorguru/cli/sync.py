from time import perf_counter_ns
from functools import wraps

import click

from juniorguru.lib import loggers
from juniorguru.lib.cli import command_name, import_commands
from juniorguru.models.base import db
from juniorguru.models.sync import Sync
from juniorguru import sync as sync_package

try:
    import pync
except (Exception, ImportError):
    pync = None


NOTIFY_AFTER_MIN = 1


logger = loggers.from_path(__file__)


class Group(click.Group):
    sync_package = sync_package

    def __init__(self, *args, **kwargs):
        self._sync_commands = None
        super().__init__(*args, **kwargs)

    @property
    def sync_commands(self):
        if self._sync_commands is None:
            self._sync_commands = dict(import_commands(self.sync_package))
        return self._sync_commands

    @property
    def dependencies_map(self):
        return {name: command.dependencies for name, command in self.sync_commands.items()}

    def sync_command(self, *args, **kwargs):
        def decorator(fn):
            @wraps(fn)
            @click.pass_context
            def wrapper(context, *fn_args, **fn_kwargs):
                name, sync = context.info_name, context.obj['sync']

                if self._is_sync_command_seen(name, sync):
                    logger[name].info('Skipping (already executed)')
                    return

                dependencies = self._get_sync_command_dependencies(name, sync)
                if dependencies:
                    logger[name].info(f"Dependencies: {', '.join(dependencies)}")
                    for dependency_name in dependencies:
                        logger[name].debug(f"Invoking dependency: {dependency_name}")
                        context.invoke(main.get_command(context, dependency_name))

                logger[name].debug('Invoking self')
                self._start_sync_command(name, sync)
                try:
                    context.invoke(fn, *fn_args, **fn_kwargs)
                finally:
                    sync_command = self._end_sync_command(name, sync)
                    logger[name].info(f"Finished in {sync_command.time_diff_min:.1f}min")
            return self.command(*args, cls=Command, **kwargs)(wrapper)
        return decorator

    @db.connection_context()
    def _is_sync_command_seen(self, name, sync):
        return sync.is_command_seen(name)

    @db.connection_context()
    def _get_sync_command_dependencies(self, name, sync):
        return list(filter(sync.is_command_unseen, self.dependencies_map[name]))

    @db.connection_context()
    def _start_sync_command(self, name, sync):
        return sync.command_start(name, perf_counter_ns())

    @db.connection_context()
    def _end_sync_command(self, name, sync):
        return sync.command_end(name, perf_counter_ns())

    def list_commands(self, context):
        return sorted(super().list_commands(context) + list(self.sync_commands))

    def get_command(self, context, name):
        return super().get_command(context, name) or self.sync_commands[name]


class Command(click.Command):
    def __init__(self, *args, dependencies=None, **kwargs):
        self.dependencies = list(dependencies or [])
        super().__init__(*args, **kwargs)
        self.name = command_name(self.callback.__module__)


@click.group(chain=True, cls=Group)
@click.option('--id', envvar='CIRCLE_BUILD_NUM', default=perf_counter_ns)
@click.pass_context
def main(context, id):
    with db.connection_context():
        sync = Sync.start(id)
    context.obj = dict(sync=sync)
    logger.info(f"Sync #{id} starts with {sync.count_commands()} commands already recorded")
    context.call_on_close(close)


@main.command()
@click.argument('job', type=click.Choice(['sync-1', 'sync-2']), envvar='CIRCLE_JOB')
@click.argument('node_index', type=int, envvar='CIRCLE_NODE_INDEX')
@click.option('--nodes', type=int, envvar='CIRCLE_NODE_TOTAL')
@click.option('--dry-run', is_flag=True, default=False, show_default=True)
@click.pass_context
def ci(context, job, node_index, nodes, dry_run):
    if job == 'sync-1':
        commands_with_deps = {name for name, deps in main.dependencies_map.items() if deps}
        chains = get_parallel_chains(main.dependencies_map, exclude=commands_with_deps)
    elif job == 'sync-2':
        commands_without_deps = {name for name, deps in main.dependencies_map.items() if not deps}
        chains = get_parallel_chains(main.dependencies_map, exclude=commands_without_deps)
    else:
        raise ValueError(job)

    if nodes and nodes != len(chains):
        logger.error(f"The job {job} has parallelism {nodes}, but there are {len(chains)} command chains!")
        raise click.Abort()

    if dry_run:
        for index, chain in enumerate(chains):
            for name in chain:
                bold, color = (True, 'green') if index == node_index else (None, None)
                click.secho(f"{index} {name}", bold=bold, fg=color)
    else:
        for name in chains[node_index]:
            command = main.get_command(context, name)
            context.invoke(command)


@main.command()
@click.option('--dry-run', is_flag=True, default=False, show_default=True)
@click.pass_context
def all(context, dry_run):
    for name in main.dependencies_map:
        command = main.get_command(context, name)
        if dry_run:
            click.echo(name)
        else:
            context.invoke(command)


@click.pass_context
def close(context):
    sync = context.obj['sync']
    logger.info(f"Sync #{sync.id} done with {sync.count_commands()} commands recorded")
    times = sync.times_min()
    if times:
        times_repr = ', '.join([f"{name} {time:.1f}min" for name, time in times.items()])
        logger.info(times_repr)
        total_time = sum(times.values())
        if total_time >= NOTIFY_AFTER_MIN:
            notify('Finished!', f'{total_time:.1f}min')


def notify(title, text):
    print('\a', end='', flush=True)
    if pync:
        pync.Notifier.notify(text, title=title)


def get_parallel_chains(dependencies_map, exclude=None):
    exclude = exclude or []
    temp_chains = {name: set([name] +
                             [c for c in deps if c not in exclude])
                   for name, deps
                   in dependencies_map.items()
                   if name not in exclude}
    chains = {}
    while True:
        seen_names = []
        for name, chain in temp_chains.items():
            if name not in seen_names:
                seen_names.append(name)
                for other_name, other_chain in temp_chains.items():
                    if other_name not in seen_names and other_chain & chain:
                        chain |= other_chain
                        seen_names.append(other_name)
                chains[name] = chain
        if len(chains) == len(temp_chains):
            return sorted(map(sorted, chains.values()))
        temp_chains = chains
        chains = {}
