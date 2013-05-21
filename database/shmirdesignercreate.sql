DROP TABLE backbone;
DROP DATABASE shmird;
CREATE DATABASE shmird;

CREATE TABLE backbone (
    id SERIAL PRIMARY KEY,
    name varchar(10) NOT NULL,
    flanks3_s varchar(80) NOT NULL,
    flanks3_a varchar(80) NOT NULL,
    flanks5_s varchar(80) NOT NULL,
    flanks5_a varchar(80) NOT NULL,
    loop_s varchar(30) NOT NULL,
    loop_a varchar(30) NOT NULL,
    miRNA_s varchar(30) NOT NULL,
    miRNA_a varchar(30) NOT NULL,
    miRNA_length integer NOT NULL,
    miRNA_min integer NOT NULL,
    miRNA_max integer NOT NULL,
    structure varchar(200) NOT NULL,
    homogeneity integer NOT NULL,
    miRBase_link varchar(200) NOT NULL
);

INSERT INTO backbone VALUES
    ('miR-30', 'TGCCTACTGCCTCGGACTTCAAGGGGCTACTTTAGGAGCA', 'TGCTCCTAAAGTAGCCCCTTGAAGTCCGAGGCAGTAGGCA',
    'CTAAAGAAGGTATATTGCTGTTGACAGTGAGCGAC', 'GTCGCTCACTGTCAACAGCAATATACCTTCTTTAG',
    'cugugaagccacagauggg', 'cccatctgtggcttcacag', 'uguaaacauccucgacuggaag', 'cttccagtcgaggatgtttaca',
    22, 19, 25, '/structures/mir30.rnaml', 2, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000088'
    
);
