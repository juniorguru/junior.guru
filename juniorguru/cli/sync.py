from time import perf_counter_ns
import pkgutil

import click

from juniorguru.lib.cli import BaseGroup
from juniorguru.lib import loggers
from juniorguru import sync as sync_package
from juniorguru.models.base import db
from juniorguru.models.sync import Sync

try:
    import pync
except (Exception, ImportError):
    pync = None


NOTIFY_AFTER_MIN = 1


logger = loggers.get(__name__)


class Group(BaseGroup):
    command_package = sync_package

    def load_dynamic_commands(self):
        for finder, name, is_package in pkgutil.iter_modules(self.command_package.__path__):
            module = finder.find_module(name).load_module(name)
            yield name.replace('_', '-'), module.main

    def dependencies_map(self, context):
        for name in self.list_commands(context):
            command = self.get_command(context, name)
            if isinstance(command, Command):
                yield name, command.requires


class Command(click.Command):
    def __init__(self, *args, **kwargs):
        self.requires = list(kwargs.pop('requires', []))
        super().__init__(*args, **kwargs)

    def invoke(self, context):
        group = context.parent.command
        name = context.info_name
        sync = context.obj['sync']

        with db.connection_context():
            if sync.is_command_seen(name):
                logger[name].debug('Skipping (already executed)')
                return
            requires = list(filter(sync.is_command_unseen, self.requires))
            if requires:
                logger[name].info(f"Dependencies: {', '.join(requires)}")
                for dep_name in requires:
                    logger[name].debug(f"Invoking: {dep_name}")
                    context.invoke(group.get_command(context, dep_name))
            sync.command_start(name, perf_counter_ns())

        try:
            return super().invoke(context)
        finally:
            with db.connection_context():
                sync_command = sync.command_end(name, perf_counter_ns())
            logger[name].debug(f"Finished in {sync_command.time_diff_min:.1f}min")


@click.group(cls=Group, chain=True)
@click.option('--id', envvar='CIRCLE_BUILD_NUM', default=perf_counter_ns)
@click.pass_context
def main(context, id):
    logger.debug(f"Sync ID: {id}")
    with db.connection_context():
        sync = Sync.start(id)
    context.obj = {'sync': sync}
    context.call_on_close(close)


@main.command()
@click.argument('job', type=click.Choice(['sync-1', 'sync-2']), envvar='CIRCLE_JOB')
@click.argument('node_index', type=int, envvar='CIRCLE_NODE_INDEX')
@click.option('--nodes', type=int, envvar='CIRCLE_NODE_TOTAL')
@click.pass_context
def ci(context, job, node_index, nodes):
    group = context.parent.command
    dependencies_map = dict(group.dependencies_map(context))

    if job == 'sync-1':
        commands_with_deps = {name for name, deps in dependencies_map.items() if deps}
        chains = get_parallel_chains(dependencies_map, exclude=commands_with_deps)
    elif job == 'sync-2':
        commands_without_deps = {name for name, deps in dependencies_map.items() if not deps}
        chains = get_parallel_chains(dependencies_map, exclude=commands_without_deps)
    else:
        raise ValueError(job)

    if nodes and nodes != len(chains):
        logger.error(f"The job {job} has parallelism {nodes}, but there are {len(chains)} command chains!")
        raise click.Abort()

    for name in chains[node_index]:
        command = group.get_command(context, name)
        context.invoke(command)


@main.command()
@click.pass_context
def all(context):
    group = context.parent.command
    for name in dict(group.dependencies_map(context)).keys():
        command = group.get_command(context, name)
        context.invoke(command)


@click.pass_context
def close(context):
    logger.info('Sync done!')
    sync = context.obj['sync']
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
