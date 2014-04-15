from Bio.Blast import NCBIWWW, NCBIXML
import cStringIO



def Blast_offtarget(fasta_string):
    result_handle = NCBIWWW.qblast("blastn", "refseq_rna", fasta_string, entrez_query="txid9606 [ORGN]", megablast=True)
    blast_results = result_handle.read()
    blast_in = cStringIO.StringIO(blast_results)
    for record in NCBIXML.parse(blast_in):
        print "QUERY: %s" % record.query
        for align in record.alignments :
            print " MATCH: %s..." % align.title[:60]
            for hsp in align.hsps :
                print " HSP, e=%f, from position %i to %i" \
                    % (hsp.expect, hsp.query_start, hsp.query_end)
                if hsp.align_length < 60 :
                     print "  Query: %s" % hsp.query
                     print "  Match: %s" % hsp.match
                     print "  Sbjct: %s" % hsp.sbjct
                else :
                     print "  Query: %s..." % hsp.query[:57]
                     print "  Match: %s..." % hsp.match[:57]
                     print "  Sbjct: %s..." % hsp.sbjct[:57]
    print "Done"
    
    
fasta_string="TTGCTGTGTGAGGCAGAACCTGCGGGGGCAGGGGCGGGCTGGTTCCCTGGCCAGCCATTGGCAGAGTCCG"
