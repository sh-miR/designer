"""
.. module:: shmir.designer.transcript.offtarget
    :synopsis: This module connection to Blast and counting offtarget
"""
from operator import itemgetter

from Bio.Application import ApplicationError
from Bio.Blast import (
    NCBIWWW,
    NCBIXML,
)
from Bio.Blast.Applications import NcbiblastnCommandline
import cStringIO

from shmir.contextmanagers import blast_path
from shmir.async import task
from shmir.data.models import (
    db_session,
    Utr
)


@task(bind=True, max_retries=10)
def blast_offtarget(self, fasta_string, with_references=False):
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

        references = []
        for line in[line for line in stdout.split('\n') if 'Homo sapiens' in line]:
            references.append(line.split('|'[3]))

        if with_references:
            return {
                'count': len(references),
                'refereces': references
            }
        return len(references)

    except ApplicationError:
        try:
            result_handle = NCBIWWW.qblast(
                "blastn", "refseq_rna", fasta_string,
                entrez_query="txid9606 [ORGN] NOT(environmental samples[organism] OR metagenomes[orgn]",
                word_size=len(fasta_string), megablast=True
            )
        except ValueError as exc:
            raise self.retry(exc=exc)

        blast_results = result_handle.read()

        blast_in = cStringIO.StringIO(blast_results)
        count = 0
        references = set()
        for record in NCBIXML.parse(blast_in):
            for align in record.alignments:
                references.add(align.accession)
                count += 1

        if with_references:
            return {
                'count': count,
                'references': references
            }
        return count


@task
def offtarget_seed(fasta_string, with_references=False):
    """Function which calculates offtarget using seed sequence on 3'UTR database

    Args:
        fasta_string(str): Fasta sequence.
        with_references(bool):

    Returns:
        Offtarget value(int).

    """
    references = db_session.query(Utr.reference).filter(
        Utr.sequence.like("%{}%".format(fasta_string[1:9].lower()))
    )
    count = len(references)
    if with_references:
        return {
            'count': count,
            'references': map(itemgetter(0), references)
        }

    return count
