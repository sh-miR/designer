"""
.. module:: shmir.designer.offtarget
    :synopsis: This module connection to Blast and counting offtarget
"""

from Bio.Application import ApplicationError
from Bio.Blast import (
    NCBIWWW,
    NCBIXML,
)
from Bio.Blast.Applications import NcbiblastnCommandline
import cStringIO

from shmir.contextmanagers import blast_path


def blast_offtarget(fasta_string):
    """Function which count offtarget using blast.

    Args:
        fasta_string(str): Fasta sequence.

    Returns:
        Offtarget value(int).
    """
    try:
        with blast_path():
            with open('fasta', 'w') as fasta_file:
                fasta_file.write(fasta_string)
            cline = NcbiblastnCommandline(
                query="fasta", db="refseq_rna",
                outfmt=("'6 qseqid sseqid evalue bitscore sgi sacc staxids"
                        "sscinames scomnames stitle'"))
            stdout, stderr = cline()

        blast_lines = [
            line for line in stdout.split('\n')
            if 'Homo sapiens' in line
        ]

        return len(blast_lines)
    except ApplicationError:
        result_handle = NCBIWWW.qblast(
            "blastn", "refseq_rna", fasta_string,
            entrez_query="txid9606 [ORGN]", expect=100, gapcosts="5 2",
            genetic_code=1, hitlist_size=100,
            word_size=len(fasta_string), megablast=True
        )
        blast_results = result_handle.read()

        blast_in = cStringIO.StringIO(blast_results)
        count = 0

        for record in NCBIXML.parse(blast_in):
            for align in record.alignments:
                count += 1
        return count
