#!/usr/bin/env python2.7

DEBUG = True


from flask import Flask

import database.handlers


app = Flask(__name__)


app.add_url_rule('/database/get_all', 'database.get_all',
                 database.handlers.get_all)
app.add_url_rule('/database/get_by_name', 'database.get_by_name',
                 database.handlers.get_by_name)
app.add_url_rule('/database/get_by_mirna_s', 'database.get_by_miRNA_s',
                 database.handlers.get_by_miRNA_s)


if __name__ == '__main__':
    app.run()
