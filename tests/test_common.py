"""Unit tests for morphoeval.cooccurrence"""

import unittest

from numpy.testing import assert_array_equal

from morphoeval.common import *


class TestAnalysisSet(unittest.TestCase):

    def _create_set(self, data):
        aset = AnalysisSet()
        for word, alts in data.items():
            for morphs in alts:
                aset.add(word, morphs)
        return aset
    
    def test_1(self):
        aset = self._create_set({
            'koira': [['koira']],
            'koiran': [['koira', 'n']],
            'koiralle': [['koira', 'lle']],
            'koirakin': [['koira', 'kin'], ['koi', 'raki', 'n']],
            'kissa': [['kissa']],
            'kissalle': [['kissa', 'lle']],
            'hiiri': [['hiiri']]
        })
        windex = aset.get_word_index()
        self.assertEqual(len(windex), 7)
        word_morpheme_mat = aset.to_word_morpheme_matrix(windex)
        self.assertEqual(word_morpheme_mat.shape, (7, 8))
        word_mat = aset.to_word_matrix(windex)
        self.assertEqual(word_mat.shape, (7, 7))

        arr = aset.common_morphs_array(aset.analyses['koira'], aset.analyses['koiralle'])
        assert_array_equal(arr, np.array([[1]]))
        arr = aset.common_morphs_array(aset.analyses['koirakin'], aset.analyses['koira'])
        assert_array_equal(arr, np.array([[1], [0]]))
        arr = aset.common_morphs_array(aset.analyses['koirakin'], aset.analyses['koiran'])
        assert_array_equal(arr, np.array([[1], [1]]))
        
        sim_mat = aset.word_similarity_matrix('koira', windex)
        self.assertEqual(sim_mat.shape, (7, 1))
        sim_mat = aset.word_similarity_matrix('koirakin', windex)
        self.assertEqual(sim_mat.shape, (7, 2))

