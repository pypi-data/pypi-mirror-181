class TorDataDirectoryException(Exception):
    '''Raised if an error with the TOR data directory occours (usually OSError)'''
    pass

class TorHashingException(Exception):
    '''Raised if TOR fails to hash a password'''
    pass

class TorStartFailedException(Exception):
    '''Raised if TOR fails to startup'''
    pass
