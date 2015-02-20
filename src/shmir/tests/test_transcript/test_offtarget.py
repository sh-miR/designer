import unittest
from mock import (
    patch,
    MagicMock
)

from Bio.Application import ApplicationError
from shmir.designer.transcript.offtarget import blast_offtarget


class TestBlastOfftarget(unittest.TestCase):

    def return_string(self):
        return 'ptakiHomo sapiens\nlataja\kluczem\nHomo sapiens', 'err'

    @patch('shmir.designer.transcript.offtarget.NcbiblastnCommandline')
    def test_blast_offtarget_correct(self, mock_ncbi_cl):
        expected_result = self.return_string()[0].count('Homo sapiens')
        mock_ncbi_cl.return_value = self.return_string
        blast_lines = blast_offtarget('fasta_string')
        self.assertEqual(blast_lines, expected_result)

    @patch('shmir.designer.transcript.offtarget.NCBIXML')
    @patch('shmir.designer.transcript.offtarget.NCBIWWW')
    @patch('shmir.designer.transcript.offtarget.NcbiblastnCommandline')
    def test_blast_offtarget_app_error(
        self, mock_ncbi_cl, mock_qblast, mock_xml
    ):
        mock_ncbi_cl.side_effect = ApplicationError('yoy', 'yoy')
        mock_xml.parse.return_value = ''
        mock_read = MagicMock()
        mock_read.read.return_value = ''
        mock_qblast.qblast.return_value = mock_read
        blast_count = blast_offtarget('fasta_string')

        self.assertEqual(blast_count, 0)
