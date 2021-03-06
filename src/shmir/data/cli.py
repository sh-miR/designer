from shmir.data import download
from shmir.data.models import (
    db_session,
    Backbone,
    Immuno,
    Utr,
    HumanmRNA
)
from shmir.data.parsers import (
    parse_utr_database,
    parse_mRNA_database
)


def seed_initial_data():
    backbones = [
        Backbone(
            name='miR-30a',
            flanks3_s='TGCCTACTGCCTCGGACTTCAAGGGGCTACTTTAGGAGCA',
            flanks3_a='TGCTCCTAAAGTAGCCCCTTGAAGTCCGAGGCAGTAGGCA',
            flanks5_s='CTAAAGAAGGTATATTGCTGTTGACAGTGAGCGAC',
            flanks5_a='GTCGCTCACTGTCAACAGCAATATACCTTCTTTAG',
            loop_s='CTGTGAAGCCACAGATGGG',
            loop_a='CCCATCTGTGGCTTCACAG',
            miRNA_s='UGUAAACAUCCUCGACUGGAAG',
            miRNA_a='CTTCCAGTCGAGGATGTTTGCAGC',
            miRNA_length=22,
            miRNA_min=19,
            miRNA_max=25,
            miRNA_end_5=-2,
            miRNA_end_3=0,
            structure='./data/structures/miR-30a',
            homogeneity=4,
            miRBase_link=('http://www.mirbase.org/cgi-bin/mirna_entry.pl'
                          '?acc=MI0000088'),
            active_strand=3
        ),
        Backbone(
            name='miR-155',
            flanks3_s=('GTGTATGATGCCTGTTACTAGCATTCACATGGAACAAATTGCTGCTGCCGTGGG'
                       'AGGATGACAAAGA'),
            flanks3_a=('TCTTTGTCATCCTCCCACGGCAGCAGCAATTTGTTCCATGTGAATGCTAGTAAC'
                       'AGGCATCATACAC'),
            flanks5_s='AGGCTTGCTGTAGGCTGTATGCTG',
            flanks5_a='CAGCATACCTACAGCAAGCCT',
            loop_s='TTTTGCCTCCAACTGA',
            loop_a='TCAGTTGGAGGCAAAA',
            miRNA_s='UUAAUGCUAAUCGUGAUAGGGGU',
            miRNA_a='CUCCUACAUAUUAGCAUUAACA',
            miRNA_length=23,
            miRNA_min=20,
            miRNA_max=26,
            miRNA_end_5=-2,
            miRNA_end_3=1,
            structure='./data/structures/miR-155',
            homogeneity=5,
            miRBase_link=('http://www.mirbase.org/cgi-bin/mirna_entry.pl'
                          '?acc=MIMAT0000646'),
            active_strand=5
        ),
        Backbone(
            name='miR-21',
            flanks3_s='CTGACATTTTGGTATCTTTCATCTGACCATCCATATCCAATGTTCTCATT',
            flanks3_a='AATGAGAACATTGGATATGGATGGTCAGATGAAAGATACCAAAATGTCAG',
            flanks5_s='TACCATCGTGACATCTCCATGGCTGTACCACCTTGTCGGG',
            flanks5_a='CCCGACAAGGTGGTACAGCCATGGAGATGTCACGATGGTA',
            loop_s='CTGTTGAATCTCATGG',
            loop_a='CCATGAGATTCAACAG',
            miRNA_s='UAGCUUAUCAGACUGAUGUUGA',
            miRNA_a='CAACACCAGUCGAUGGGCUGU',
            miRNA_length=22,
            miRNA_min=19,
            miRNA_max=24,
            miRNA_end_5=-1,
            miRNA_end_3=1,
            structure='./data/structures/miR-21',
            homogeneity=4,
            miRBase_link=('http://www.mirbase.org/cgi-bin/mirna_entry.pl'
                          '?acc=MI0000077'),
            active_strand=5
        ),
        Backbone(
            name='miR-122',
            flanks3_s='GCTACTGCTAGGCAATCCTTCCCTCGATAAATGTCTTGGCATCGTTTGCTT',
            flanks3_a='AAGCAAACGATGCCAAGACATTTATCGAGGGAAGGATTGCCTAGCAGTAGC',
            flanks5_s='TGGAGGTGAAGTTAACACCTTCGTGGCTACAGAGTTTCCTTAGCAGAGCTG',
            flanks5_a='CAGCTCTGCTAAGGAAACTCTGTAGCCACGAAGGTGTTAACTTCACCTCCA',
            loop_s='TGTCTAAACTATCA',
            loop_a='TGATAGTTTAGACA',
            miRNA_s='UGGAGUGUGACAAUGGUGUUUG',
            miRNA_a='AACGCCAUUAUCACACUAAAUA',
            miRNA_length=22,
            miRNA_min=21,
            miRNA_max=23,
            miRNA_end_5=-2,
            miRNA_end_3=2,
            structure='./data/structures/miR-122',
            homogeneity=5,
            miRBase_link=('http://www.mirbase.org/cgi-bin/mirna_entry.pl'
                          '?acc=MI0000442'),
            active_strand=5
        ),
        Backbone(
            name='miR-31',
            flanks3_s='CTTTCCTGTCTGACAGCAGCTTGGCTACCTCCGTCCTGTTCCTCCTTGTCTT',
            flanks3_a='AAGACAAGGAGGAACAGGACGGAGGTAGCCAAGCTGCTGTCAGACAGGAAAG',
            flanks5_s='CATAACAACGAAGAGGGATGGTATTGCTCCTGTAACTCGGAACTGGAGAGG',
            flanks5_a='CCTCTCCAGTTCCGAGTTACAGGAGCAATACCATCCCTCTTCGTTGTTATG',
            loop_s='GTTGAACTGGGAACC',
            loop_a='GGTTCCCAGTTCAAC',
            miRNA_s='AGGCAAGAUGCUGGCAUAGCU',
            miRNA_a='UGCUAUGCCAACAUAUUGCCAU',
            miRNA_length=21,
            miRNA_min=19,
            miRNA_max=23,
            miRNA_end_5=-1,
            miRNA_end_3=1,
            structure='./data/structures/miR-31',
            homogeneity=4,
            miRBase_link=('http://www.mirbase.org/cgi-bin/mirna_entry.pl'
                          '?acc=MI0000089'),
            active_strand=5
        ),
        Backbone(
            name='miR-26a',
            flanks3_s='GGGACGC',
            flanks3_a='GCGTCCC',
            flanks5_s='GTGGCCTCG',
            flanks5_a='CGAGGCCAC',
            loop_s='GTGCAGGTCCCAATGGG',
            loop_a='CCCATTGGGACCTGCAC',
            miRNA_s='UUCAAGUAAUCCAGGAUAGGCU',
            miRNA_a='CCUAUUCUUGGUUACUUGCACG',
            miRNA_length=22,
            miRNA_min=21,
            miRNA_max=23,
            miRNA_end_5=-2,
            miRNA_end_3=2,
            structure='./data/structures/miR-26a',
            homogeneity=4,
            miRBase_link=('http://www.mirbase.org/cgi-bin/mirna_entry.pl'
                          '?acc=MI0000083'),
            active_strand=5
        ),
        Backbone(
            name='miR-106b',
            flanks3_s='TCCAGCAGG',
            flanks3_a='CCTGCTGGA',
            flanks5_s='CCTGCCGGGGC',
            flanks5_a='GCCCCGGCAGG',
            loop_s='AGTGGTCCTCTCCGTGCTA',
            loop_a='TAGCACGGAGAGGACCACT',
            miRNA_s='UAAAGUGCUGACAGUGCAGAU',
            miRNA_a='CCGCACUGUGGGUACUUGCUGC',
            miRNA_length=21,
            miRNA_min=20,
            miRNA_max=22,
            miRNA_end_5=-3,
            miRNA_end_3=2,
            structure='./data/structures/miR-106b',
            homogeneity=2,
            miRBase_link=('http://www.mirbase.org/cgi-bin/mirna_entry.pl'
                          '?acc=MI0000734'),
            active_strand=0
        )
    ]
    immunos = [
        Immuno(
            sequence='UGUGU',
            receptor='TLR7 and TLR8',
            link='http://www.ncbi.nlm.nih.gov/pubmed/16609928'
        ),
        Immuno(
            sequence='GUCCUUCAA',
            receptor='TLR7 and TLR8',
            link='http://www.ncbi.nlm.nih.gov/pubmed/15723075'
        ),
        Immuno(
            sequence='GU',
            receptor='TLR7 and TLR8',
            link='http://www.ncbi.nlm.nih.gov/pubmed/16609928'
        ),
        Immuno(
            sequence='AU',
            receptor='TLR8',
            link='http://www.ncbi.nlm.nih.gov/pubmed/18322178'
        ),
        Immuno(
            sequence='UGGC',
            receptor='',
            link='http://www.ncbi.nlm.nih.gov/pubmed/16682561'
        ),
        Immuno(
            sequence='UUUUU',
            receptor='',
            link='http://www.ncbi.nlm.nih.gov/pubmed/15778705'
        )
    ]

    if db_session.query(Utr).count() == 0:
        filename = download.download_utr_database()
        for sequence, reference in parse_utr_database(filename):
            db_session.add(
                Utr(
                    sequence=sequence,
                    reference=reference
                )
            )
    if db_session.query(HumanmRNA).count() == 0:
        filename = download.download_human_all_database()
        for sequence, reference in parse_mRNA_database(filename):
            db_session.add(
                HumanmRNA(
                    sequence=sequence,
                    reference=reference
                )
            )

    if db_session.query(Backbone).count() == 0:
        db_session.add_all(backbones)
    if db_session.query(Immuno).count() == 0:
        db_session.add_all(immunos)
    db_session.commit()


def main():
    seed_initial_data()
