import os

from rpcpdb import updb

from shmir import settings


def set_trace():
    sock_path = settings.PDB_SOCKET
    try:
        os.remove(sock_path)
    except OSError:
        pass
    updb.UPdb(sock_path=sock_path).set_trace()
