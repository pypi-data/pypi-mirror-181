import click
from vijay_dir.vijay_logic import configure,run,status


@click.group()
def main():
    """  The  aitest  Command  Line  Interface is a unified tool to manage your aitest
         services.

        To see help text, you can run:

        vijay --help\n
        vijay <command> --help\n
        vijay <command> <subcommand> --help\n

    """

#adding subcommands 
main.add_command(configure)
main.add_command(run)
main.add_command(status)
