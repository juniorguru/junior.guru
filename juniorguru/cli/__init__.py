import click

from juniorguru.cli import cancel_previous_builds, dev, web, participant, screenshots, winners, students, check_docs, check_links


@click.group()
def main():
    pass


main.add_command(dev.lint)
main.add_command(dev.format)
main.add_command(dev.test)


for module in [cancel_previous_builds,
               check_docs,
               check_links,
               web,
               participant,
               screenshots,
               winners,
               students]:
    main.add_command(module.main, name=module.__name__)
