import functools
import os
import urllib

import progressbar

from shmir import settings


def ensure_main_path(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not os.path.isdir(settings.BIO_DATABASES_PATH):
            os.mkdir(settings.BIO_DATABASES_PATH)
        return f(*args, **kwargs)
    return wrapper


def download_file(base_name, url):
    full_path = os.path.join(settings.BIO_DATABASES_PATH,
                             base_name)
    if os.path.exists(full_path):
        return full_path

    widgets = [base_name,
               progressbar.Percentage(),
               ' ',
               progressbar.Bar(),
               ' ',
               progressbar.ETA(),
               ' ',
               progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets)

    def download_progress(count, block_size, total_size):
        if pbar.maxval is None:
            pbar.maxval = total_size
            pbar.start()
        pbar.update(min(count * block_size, total_size))

    full_path, _ = urllib.urlretrieve(url, full_path, reporthook=download_progress)
    pbar.finish()
    return full_path


@ensure_main_path
def download_utr_database():
    base_name = '3UTRaspic.Hum.dat.gz'
    url = 'http://ftp.ebi.ac.uk/pub//databases/UTR/data/3UTRaspic.Hum.dat.gz'
    return download_file(base_name, url)


@ensure_main_path
def download_human_all_database():
    base_name = 'human_all.fna.gz'
    url = 'https://dl.dropboxusercontent.com/s/cowuibi385f0ddd/human_all.fna.gz'
    return download_file(base_name, url)
