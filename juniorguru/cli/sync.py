from time import perf_counter
from functools import wraps
import pkgutil

import click

from juniorguru.lib import loggers
from juniorguru import sync as sync_package

try:
    import pync
except (Exception, ImportError):
    pync = None


NOTIFY_AFTER_SEC = 60


logger = loggers.get(__name__)


class SyncGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.chains_exclude = []

    def sync_command(self, *args, **kwargs):
        def decorator(fn):
            @wraps(fn)
            def wrapper(*fn_args, **fn_kwargs):
                context = click.get_current_context()
                command_name = context.command.name
                logger_c = logger[command_name]

                if command_name in context.obj['timing']:
                    logger_c.debug('Skipping (already executed)')
                    return

                dependencies = (set(self.dependencies[command_name])
                                - set(context.obj['timing'].keys()))
                if dependencies:
                    logger_c.info(f"Dependencies: {', '.join(dependencies)}")
                    if context.obj['interactive']:
                        click.confirm('Continue?', abort=True)
                    for dependency in dependencies:
                        logger_c.debug(f"Invoking: {dependency}")
                        context.invoke(self.get_command(context, dependency))

                t0 = perf_counter()
                fn(*fn_args, **fn_kwargs)
                t = perf_counter() - t0

                logger_c.debug(f"Finished in {t / 60:.1f}min")
                context.obj['timing'][command_name] = t

                if context.obj['interactive'] and t >= NOTIFY_AFTER_SEC:
                    notify(f'Finished: sync {command_name}!', f'{t / 60:.1f}min')

            kwargs.setdefault('name', fn.__module__.split('.')[-1].replace('_', '-'))  # duplicate?
            self.dependencies[kwargs['name']] = kwargs.pop('requires', [])
            return self.command(*args, **kwargs)(wrapper)
        return decorator

    def import_commands_from(self, package):
        for finder, name, is_package in pkgutil.iter_modules(package.__path__):
            try:
                module = finder.find_module(name).load_module(name)
                if isinstance(module.main, click.Command):
                    command_name = module.__name__.split('.')[-1].replace('_', '-')  # duplicate?
                    self.add_command(module.main, name=command_name)
                else:
                    logger.debug(f"Could not import {name}, module's main is {module.main.__class__!r}")
            except Exception as e:
                logger.debug(f"Could not import {name}, {e.__class__.__name__}: {e}")


def get_parallel_chains(dependencies, exclude=None):
    exclude = exclude or []
    temp_chains = {name: set([name] +
                             [c for c in commands if c not in exclude])
                   for name, commands
                   in dependencies.items()
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


def notify(title, text):
    print('\a', end='', flush=True)
    if pync:
        pync.Notifier.notify(text, title=title)


@click.command(cls=SyncGroup, chain=True)
@click.option('--interactive/--no-interactive', envvar='INTERACTIVE_SYNC', default=False)
@click.pass_context
def main(context, interactive):
    context.obj = {'interactive': interactive,
                   'timing': {}}
    logger.debug(f"Interactive? {'YES' if interactive else 'NO'}")
    context.call_on_close(close)


@main.command()
@click.argument('phase', type=click.Choice(['all', '1', '2']), default='all')
def chains(phase):
    commands_without_deps = {name for name, commands
                             in main.dependencies.items()
                             if not commands}
    commands_with_deps = set(main.dependencies.keys()) - commands_without_deps

    if phase == 'all':
        chains = get_parallel_chains(main.dependencies)
    elif phase == '1':
        chains = get_parallel_chains(main.dependencies, exclude=commands_with_deps)
    elif phase == '2':
        chains = get_parallel_chains(main.dependencies, exclude=commands_without_deps)
    else:
        raise ValueError(phase)
    for chain in chains:
        click.echo(' '.join(chain))


@main.command()
@click.pass_context
def all(context):
    if context.obj['interactive']:
        logger.warning('Ignoring interactive mode')
        context.obj['interactive'] = False
    for name in main.dependencies.keys():
        context.invoke(main.get_command(context, name))
    logger.info('Sync done!')


@click.pass_context
def close(context):
    # if node:
    #     logger.debug(f"Node #{node}")
    pass  # TODO junit.xml, context.obj['timing']


main.import_commands_from(sync_package)
