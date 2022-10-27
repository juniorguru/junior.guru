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
    def load_dynamic_commands(self):
        for finder, name, is_package in pkgutil.iter_modules(sync_package.__path__):
            module = finder.find_module(name).load_module(name)
            yield name.replace('_', '-'), module.main

    def iter_chain_commands(self, context):
        for name in super().list_commands(context):
            command = self.get_command(context, name)
            if isinstance(command, ChainCommand):
                yield name, command


class ChainCommand(click.Command):
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

        result = super().invoke(context)

        with db.connection_context():
            sync_command = sync.command_end(name, perf_counter_ns())
        logger[name].debug(f"Finished in {sync_command.time_diff_min:.1f}min")
        return result


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
    names_commands_map = list(group.iter_chain_commands(context))
    names_dependencies_map = {name: command.requires for name, command in names_commands_map}

    if job == 'sync-1':
        exclude = {name for name, command in names_commands_map if command.requires}
        chains = get_parallel_chains(names_dependencies_map, exclude=exclude)
    elif job == 'sync-2':
        exclude = {name for name, command in names_commands_map if not command.requires}
        chains = get_parallel_chains(names_dependencies_map, exclude=exclude)
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
    for name, command in group.iter_chain_commands(context):
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


def get_parallel_chains(names_dependencies_map, exclude=None):
    exclude = exclude or []
    temp_chains = {name: set([name] +
                             [c for c in deps if c not in exclude])
                   for name, deps
                   in names_dependencies_map.items()
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
