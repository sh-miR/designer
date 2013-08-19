#!usr/bin/env python

def parser_ss(file_name):
    """Function for parse ss file and gives tuples with first
        and last column on output"""
    read_data = []
    with open(file_name, "r") as ss_file:
        for line in ss_file.readlines():
            splited = line.split()
            read_data.append((splited[0], splited[-1]))
    return read_data