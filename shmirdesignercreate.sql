DROP DATABASE shmird;
CREATE DATABASE shmird;
\c shmird;

CREATE TABLE backbone (
    "id" SERIAL PRIMARY KEY,
    "name" varchar(10) NOT NULL,
    "flanks3_s" varchar(80) NOT NULL,
    "flanks3_a" varchar(80) NOT NULL,
    "flanks5_s" varchar(80) NOT NULL,
    "flanks5_a" varchar(80) NOT NULL,
    "loop_s" varchar(30) NOT NULL,
    "loop_a" varchar(30) NOT NULL,
    "miRNA_s" varchar(30) NOT NULL,
    "miRNA_a" varchar(30) NOT NULL,
    "miRNA_length" integer NOT NULL,
    "miRNA_min" integer NOT NULL,
    "miRNA_max" integer NOT NULL,
    "miRNA_end_5" integer NOT NULL,
    "miRNA_end_3" integer NOT NULL,
    "structure" varchar(200) NOT NULL,
    "homogeneity" integer NOT NULL,
            /*homogeneity of products (length), 0 for very
             nonhomogenous, 5 for completely homogenous */
    "miRBase_link" varchar(200) NOT NULL,
    "active_strand" integer NOT NULL,
            /*5 for 5' end, 3 for 3' end, 0 for equally active,
            1 for not known*/
    "regexp" varchar(1000)
);

CREATE TABLE immuno (
    "id" serial PRIMARY KEY,
    "sequence" varchar(10) NOT NULL,
    "receptor" varchar(15),
    "link" varchar(100) NOT NULL
);

INSERT INTO immuno VALUES
    (DEFAULT, 'UGUGU', 'TLR7 and TLR8', 'http://www.ncbi.nlm.nih.gov/pubmed/16609928'
    ),
    (DEFAULT, 'GUCCUUCAA', 'TLR7 and TLR8', 'http://www.ncbi.nlm.nih.gov/pubmed/15723075'
    ),
    (DEFAULT, 'GU', 'TLR7 and TLR8', 'http://www.ncbi.nlm.nih.gov/pubmed/16609928'
    ),
    (DEFAULT, 'AU', 'TLR8', 'http://www.ncbi.nlm.nih.gov/pubmed/18322178'
    ),
    (DEFAULT, 'UGGC', '', 'http://www.ncbi.nlm.nih.gov/pubmed/16682561'
    ),
    (DEFAULT, 'UUUUU', '', 'http://www.ncbi.nlm.nih.gov/pubmed/15778705'
    );
/*Please use only uppercase letters in sequences*/
INSERT INTO backbone VALUES
    (DEFAULT, 'miR-30a', 'TGCCTACTGCCTCGGACTTCAAGGGGCTACTTTAGGAGCA', 'TGCTCCTAAAGTAGCCCCTTGAAGTCCGAGGCAGTAGGCA',
    'CTAAAGAAGGTATATTGCTGTTGACAGTGAGCGAC', 'GTCGCTCACTGTCAACAGCAATATACCTTCTTTAG',
    'CTGTGAAGCCACAGATGGG', 'CCCATCTGTGGCTTCACAG', 'UGUAAACAUCCUCGACUGGAAG', 'CTTCCAGTCGAGGATGTTTGCAGC',
    22, 19, 25, -2, 0, '/structures/miR-30a', 4, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000088', 3
    ),
    (DEFAULT, 'miR-155', 'GTGTATGATGCCTGTTACTAGCATTCACATGGAACAAATTGCTGCTGCCGTGGGAGGATGACAAAGA',
    'TCTTTGTCATCCTCCCACGGCAGCAGCAATTTGTTCCATGTGAATGCTAGTAACAGGCATCATACAC',
    'AGGCTTGCTGTAGGCTGTATGCTG', 'CAGCATACCTACAGCAAGCCT',
    'TTTTGCCTCCAACTGA', 'TCAGTTGGAGGCAAAA', 'UUAAUGCUAAUCGUGAUAGGGGU', 'CUCCUACAUAUUAGCAUUAACA',
    23, 20, 26, -2, 1,  '/structures/miR-155', 5, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MIMAT0000646', 5
    ),
    (DEFAULT, 'miR-21', 'CTGACATTTTGGTATCTTTCATCTGACCATCCATATCCAATGTTCTCATT', 'AATGAGAACATTGGATATGGATGGTCAGATGAAAGATACCAAAATGTCAG',
    'TACCATCGTGACATCTCCATGGCTGTACCACCTTGTCGGG', 'CCCGACAAGGTGGTACAGCCATGGAGATGTCACGATGGTA',
    'CTGTTGAATCTCATGG', 'CCATGAGATTCAACAG', 'UAGCUUAUCAGACUGAUGUUGA', 'CAACACCAGUCGAUGGGCUGU',
    22, 19, 24, -1, 1,  '/structures/miR-21', 4, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000077', 5),
    (DEFAULT, 'miR-122', 'GCTACTGCTAGGCAATCCTTCCCTCGATAAATGTCTTGGCATCGTTTGCTT', 'AAGCAAACGATGCCAAGACATTTATCGAGGGAAGGATTGCCTAGCAGTAGC',
    'TGGAGGTGAAGTTAACACCTTCGTGGCTACAGAGTTTCCTTAGCAGAGCTG', 'CAGCTCTGCTAAGGAAACTCTGTAGCCACGAAGGTGTTAACTTCACCTCCA',
    'TGTCTAAACTATCA', 'TGATAGTTTAGACA', 'UGGAGUGUGACAAUGGUGUUUG', 'AACGCCAUUAUCACACUAAAUA',
    22, 21, 23, -2, 2,  '/structures/miR-122', 5, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000442', 5),
    (DEFAULT, 'miR-31', 'CTTTCCTGTCTGACAGCAGCTTGGCTACCTCCGTCCTGTTCCTCCTTGTCTT',
    'AAGACAAGGAGGAACAGGACGGAGGTAGCCAAGCTGCTGTCAGACAGGAAAG',
    'CATAACAACGAAGAGGGATGGTATTGCTCCTGTAACTCGGAACTGGAGAGG', 'CCTCTCCAGTTCCGAGTTACAGGAGCAATACCATCCCTCTTCGTTGTTATG',
    'GTTGAACTGGGAACC', 'GGTTCCCAGTTCAAC', 'AGGCAAGAUGCUGGCAUAGCU', 'UGCUAUGCCAACAUAUUGCCAU',
    21, 19, 23, -1, 1,  '/structures/miR-31', 4, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000089', 5);
