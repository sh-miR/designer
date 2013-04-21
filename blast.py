from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
XML = NCBIWWW.qblast("blastn", "nt", "8332116")
#print(NCBIWWW.qblast("blastn", "nt", "8332116").read()) #zwraca jako xml są parsery XML'a
blast_record = NCBIXML.read(XML)
for alignment in blast_record.alignments:
    for hsp in alignment.hsps:
        print("ALIGMENT")
        print("squence:" + alignment.title)
        print("length:", alignment.length)
        print("e value:", hsp.expect)
        print(hsp.query[:75] + "...")
        print(hsp.match[:75] + "...")
        print(hsp.sbjct[:75] + "...")

