from jg.coop.cli.sync import main as cli


@cli.sync_command(dependencies=["club-content"])
def main():
    print("Syncing meetups...")
