import gzip

from Bio import SeqIO


def parse_utr_database(filename):
    for record in SeqIO.parse(gzip.open(filename, 'r'), 'embl'):
        seq = str(record.seq)
        source = [f for f in record.features if f.type == 'source'][0]
        name = 'RefSeq:'
        ref = [s[len(name):] for s in source.qualifiers['db_xref']
               if s.startswith(name)][0]
        yield seq.upper(), ref


def parse_mRNA_database(filename):
    for record in SeqIO.parse(gzip.open(filename, 'r'), 'fasta'):
        seq = str(record.seq)
        yield seq.upper(), record.id.split("|")[-2]
