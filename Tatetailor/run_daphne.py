from daphne.cli import CommandLineInterface

def main():
    cli = CommandLineInterface()
    cli.run([
        '-b', '127.0.0.1',
        '-p', '9000',
        'Tatetailor.asgi:application'
    ])
