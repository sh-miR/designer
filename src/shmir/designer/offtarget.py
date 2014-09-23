from Bio.Blast import NCBIWWW, NCBIXML
import cStringIO



def blast_offtarget(fasta_string):
    result_handle = NCBIWWW.qblast("blastn", "refseq_rna", fasta_string, entrez_query="txid9606 [ORGN]", expect=100, gapcosts="5 2", genetic_code=1, hitlist_size=100, word_size=len(fasta_string), megablast=True)
    blast_results = result_handle.read()
    blast_in = cStringIO.StringIO(blast_results)
    count = 0
    for record in NCBIXML.parse(blast_in):
        for align in record.alignments :
            count = count + 1
    return count
    
def check_offtarget(min, max, fasta_string):
    actual_offtarget=blast_offtarget(fasta_string)
    if (actual_offtarget<=max and actual_offtarget>=min):
        return 0
    else:
        return 1
