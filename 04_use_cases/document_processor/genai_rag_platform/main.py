from src.interface.cli import run_cli
from src.config.settings import setup_logging

if __name__ == '__main__':
    setup_logging()
    run_cli()
