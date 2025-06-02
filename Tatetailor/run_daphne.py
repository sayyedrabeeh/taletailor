from daphne.cli import CommandLineInterface

def main():
    args = ['-b', '127.0.0.1', '-p', '8000', 'Tatetailor.asgi:application']
    cli = CommandLineInterface()
    cli.run(args)
