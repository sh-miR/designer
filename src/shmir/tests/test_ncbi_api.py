import json
import unittest

from mock import (
    Mock,
    patch
)

from shmir.data import ncbi_api
from shmir.designer import errors


class TestGetDataFromNcbi(unittest.TestCase):
    GOOD_MRNA = 'NM_001128164.1'
    BAD_MNRA = 'NC_000071.6'
    DATA_BASE = 'nucleotide'

    @patch.object(ncbi_api.Entrez, 'esearch')
    @patch.object(ncbi_api.Entrez, 'efetch')
    def test_get_data(self, mock_efetch, mock_esearch):
        ids = [69]
        mock_read = Mock()
        mock_read.read.return_value = json.dumps(
            {'esearchresult': {'idlist': ids}}
        )
        mock_esearch.return_value = mock_read

        ncbi_api.get_data(self.GOOD_MRNA)

        mock_esearch.assert_called_with(
            term='NM_001128164.1', db=self.DATA_BASE, retmode='json'
        )
        mock_efetch.assert_called_once_with(
            db=self.DATA_BASE, id=ids, rettype='fasta', retmode='text'
        )

    @patch.object(ncbi_api, 'get_data')
    def test_get_mRNA(self, mock_get_data):
        data_from_transcript = 'ptaki.lataja.kluczem.mRNAGACTGACTG'
        mock_get_data.return_value = data_from_transcript

        expected_string = data_from_transcript.split('mRNA')[1]
        data = ncbi_api.get_mRNA(self.GOOD_MRNA)

        mock_get_data.assert_called_once_with(self.GOOD_MRNA)
        self.assertEqual(expected_string, data)

    @patch.object(ncbi_api, 'get_data')
    def test_incorrect_get_mRNA(self, mock_get_data):
        with self.assertRaises(errors.IncorrectDataError):
            ncbi_api.get_mRNA(self.BAD_MNRA)

        self.assertEqual(len(mock_get_data.mock_calls), 0)

    @patch.object(ncbi_api, 'get_data')
    def test_no_results_get_mRNA(self, mock_get_data):
        data_from_transcript = 'ptaki.lataja.kluczem.GACTGACTG'
        mock_get_data.return_value = data_from_transcript

        with self.assertRaises(errors.NoResultError):
            ncbi_api.get_mRNA(self.GOOD_MRNA)

        mock_get_data.assert_called_once_with(self.GOOD_MRNA)
