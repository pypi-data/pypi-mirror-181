import os
from .settings import config
from .common import get_folder_by_given_name, get_folder_by_sha256
def main(db, by='given_name'):
    if by == 'given_name':
        folder = get_folder_by_given_name(db) # in which get cache first, then download from server, local is one type os server
    else:
        folder = get_folder_by_sha256(db)
    return folder
