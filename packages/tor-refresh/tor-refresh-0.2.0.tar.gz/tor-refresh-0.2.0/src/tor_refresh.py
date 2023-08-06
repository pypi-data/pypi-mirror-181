import time
import typer
from tor_refresh.tor import Tor
from tor_refresh.utils import get_secure_password

def main(port: int = typer.Argument(9150), control_port: int = typer.Argument(9151)):
    tor = Tor(port, control_port, get_secure_password(16))

    tor.start()

    print(tor.get_external_address())

    time.sleep(5)

    tor.stop()

if __name__ == '__main__':
    typer.run(main)
