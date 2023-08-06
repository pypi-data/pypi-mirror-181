'''
Create and interact with a TOR instance
'''

import os
import re
from subprocess import Popen, PIPE
import requests
from stem import Signal
from stem.control import Controller
from .exceptions import TorHashingException, TorStartFailedException, TorDataDirectoryException

class Tor:
    '''
    Simplifies the creation of TOR circuits

    Args:
    - socks_port: int (TOR SocksPort)
    - control_port: int (TOR ControlPort)
    - password: str (Password for TOR ControlPort)
    '''

    def __init__(self, socks_port: int, control_port: int, password: str):
        self.socks_port = socks_port
        self.control_port = control_port
        self.password = password
        self.is_tor_started = False
        self.tor_process = None
        self.storage_directory_path = self.__create_storage_directory__()
        self.data_directory_path = self.__create_data_directory__()
        self.hashed_password = self.__hash_password__()
        self.torrc_path = self.__create_torrc__()

    def start(self) -> None:
        '''
        Starts a TOR process listening on self.socks_port and self.control_port

        Raises:
        - TorStartFailedException
        '''

        COMMAND = ['tor', '-f', self.torrc_path]

        if self.is_tor_started:
            return

        self.tor_process = Popen(COMMAND, stdout=PIPE, stderr=PIPE)

        try: # Waiting for TOR to start
            for line in self.tor_process.stdout:
                if b'100%' in line:
                    self.is_tor_started = True
                    break
        except TypeError: # Catching iteration of NoneType
            pass

        if not self.is_tor_started: # TOR could not start
            raise TorStartFailedException

    def renew_circuit(self) -> None:
        '''Renew the TOR circuit'''

        if not self.is_tor_started:
            return

        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal['NEWNYM'])

    def stop(self) -> None:
        '''
        Kills TOR

        Raises:
        - TorDataDirectoryException
        '''

        if not self.is_tor_started:
            return

        self.tor_process.terminate()

        self.is_tor_started = False

    def get_external_address(self) -> str:
        '''Returns the IP address of the current circuit's exit node'''

        apis = [
            'https://api.ipify.org',
            'https://api.my-ip.io/ip',
            'https://checkip.amazonaws.com',
            'https://icanhazip.com',
            'https://ifconfig.me/ip',
            'https://ip.rootnet.in',
            'https://ipapi.co/ip',
            'https://ipinfo.io/ip',
            'https://myexternalip.com/raw',
            'https://trackip.net/ip',
            'https://wtfismyip.com/text'
        ]

        proxies = {
            'http': f'socks5://localhost:{self.socks_port}',
            'https': f'socks5://localhost:{self.socks_port}'
        }

        if not self.is_tor_started:
            return

        for api in apis:
            try:
                response = requests.get(api, proxies=proxies)
            except ConnectionError:
                apis.pop(apis.index(api)) # Removing API if not working
            else:
                if response.status_code in range(200, 300):
                    return response.text.strip()

                apis.pop(apis.index(api)) # Removing API if not working

    def __hash_password__(self) -> str:
        '''
        Returns TOR hashed password
        Raises:
        - TorHashingException
        '''

        COMMAND = ['tor', '--hash-password', self.password]

        with Popen(COMMAND, stdout=PIPE, stderr=PIPE) as tor_hasher:
            for line in tor_hasher.stdout:
                line = line.decode('UTF-8')
                line.strip()

                if re.match('^16:[0-9A-F]{58}$', line):
                    return line

            raise TorHashingException

    def __create_storage_directory__(self) -> str:
        '''
        Creates the program storage directory
        Raises:
        - TorDataDirectoryException
        '''

        PATH = '/tmp/tor_refresh'

        try:
            os.mkdir(PATH)
        except OSError:
            pass

        return PATH

    def __create_data_directory__(self) -> str:
        '''
        Creates a temporary TOR DataDirectory
        Raises:
        - TorDataDirectoryException
        '''

        PATH = f'{self.storage_directory_path}/{self.socks_port}'

        try:
            os.mkdir(PATH)
        except OSError:
            raise TorDataDirectoryException

        return PATH

    def __create_torrc__(self) -> str:
        '''Creates a temporary torrc file inside the program's storage directory'''

        PATH = f'{self.storage_directory_path}/torrc.{self.socks_port}'

        with open(PATH, 'w') as torrc:
            torrc.write(f'SocksPort {self.socks_port}\n')
            torrc.write(f'DataDirectory {self.data_directory_path}\n')
            torrc.write(f'ControlPort {self.control_port}\n')
            torrc.write(f'HashedControlPassword {self.hashed_password}')

        return PATH
