DROP DATABASE shmird;
CREATE DATABASE shmird;
\c shmird;

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
            /*homogeneity of products (length), 0 for very 
             nonhomogenous, 5 for completely homogenous */ 
    miRBase_link varchar(200) NOT NULL
);
/*Proszę o trzymanie się składni same wielkie bądź same małe litery w insertach*/
INSERT INTO backbone VALUES
    (DEFAULT, 'miR-30', 'TGCCTACTGCCTCGGACTTCAAGGGGCTACTTTAGGAGCA', 'TGCTCCTAAAGTAGCCCCTTGAAGTCCGAGGCAGTAGGCA',
    'CTAAAGAAGGTATATTGCTGTTGACAGTGAGCGAC', 'GTCGCTCACTGTCAACAGCAATATACCTTCTTTAG',
    'CUGUGAAGCCACAGAUGGG', 'CCCATCTGTGGCTTCACAG', 'UGUAAACAUCCUCGACUGGAAG', 'CTTCCAGTCGAGGATGTTTACA',
    22, 19, 25, '/structures/mir30.rnaml', 2, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000088'
    ),
    (DEFAULT, 'miR-155', 'TCGAGAGGCTTGCTGTAGG', 'CAGCATACAGCCTACAGCAAGCCTC',
    'TGTATGATGCCTGTTACTAGCATTCACATGGAACAAATTGCTGCCGTGGGAGGATGACAAAGAA', 'CGCGTTCTTTGTCATCCTCCCACGGCAGCAATTTGTTCCATGTGAATGCTAGTAACAG',
    'TTTTGCCTCCAACTGA', 'TCAGTTGGAGGCAAAA', 'UUAAUGCUAAUCGUGAUAGGGGU', 'TCCCCUAUCACGAUUAGCAUUAA',
    23, 20, 26, '/structures/mir155.rnaml', 4, 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MIMAT0000646'
    );
