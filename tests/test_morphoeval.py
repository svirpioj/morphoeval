"""Unit tests for morphoeval"""

import unittest

from morphoeval import *


class TestCoMMA(unittest.TestCase):
    """Test CoMMA method"""

    reference = {
        'koira': ['koira'],
        'koiran': ['koira', 'n'],
        'koiralle': ['koira', 'lle'],
        'koirakin': ['koira', 'kin'],
        'kissa': ['kissa'],
        'kissalle': ['kissa', 'lle'],
        'hiiri': ['hiiri']
    }

    def test_identical(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, morphs)
        pre, rec = comma(goldlist, predlist)
        self.assertEqual(pre, 1)
        self.assertEqual(rec, 1)

    def test_unsegmented(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, [word])
        pre, rec = comma(goldlist, predlist)
        self.assertEqual(pre, 1)
        self.assertEqual(rec, 0)

    def test_unsegmented_diag(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, [word])
        pre, rec = comma(goldlist, predlist, diagonals=True)
        self.assertEqual(pre, 1)
        self.assertAlmostEqual(rec, 11 / 30)

    def test_shared_morph(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, ['x'])
        pre, rec = comma(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.38095238)
        self.assertEqual(rec, 1)

    def test_example(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': ['koira'],
            'koiran': ['koira', 'n'],
            'koiralle': ['koira', 'lle'],
            'koirakin': ['koira', 'ki', 'n'],
            'kissa': ['ki', 'ssa'],
            'kissalle': ['kissa', 'lle'],
            'hiiri': ['hiiri']
        }
        for word, morphs in prediction.items():
            predlist.add(word, morphs)
        pre, rec = comma(goldlist, predlist)
        self.assertEqual(pre, 0.725)
        self.assertEqual(rec, 0.75)

    def test_example2(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        goldlist.add('kissassa', ['kissa', 'ssa'])
        predlist = AnalysisSet()
        prediction = {
            'koira': ['koira'],
            'koiran': ['koira', 'n'],
            'koiralle': ['koira', 'lle'],
            'koirakin': ['koira', 'ki', 'n'],
            'kissa': ['ki', 'ssa'],
            'kissalle': ['kissa', 'lle'],
            'hiiri': ['hiiri'],
            'kissassa': ['ki', 'ssa', 'ssa']
        }
        for word, morphs in prediction.items():
            predlist.add(word, morphs)
        pre, rec = comma(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.70238095)
        self.assertAlmostEqual(rec, 0.76190476)


class TestEMMA2(unittest.TestCase):
    """Test EMMA-2 method"""

    reference = {
        'koira': ['koira'],
        'koiran': ['koira', 'n'],
        'koiralle': ['koira', 'lle'],
        'koirakin': ['koira', 'kin'],
        'kissa': ['kissa'],
        'kissalle': ['kissa', 'lle'],
        'hiiri': ['hiiri']
    }

    def test_identical(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, morphs)
        pre, rec = emma2(goldlist, predlist)
        self.assertEqual(pre, 1)
        self.assertEqual(rec, 1)

    def test_unsegmented(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, [word])
        pre, rec = emma2(goldlist, predlist)
        self.assertEqual(pre, 1)
        self.assertAlmostEqual(rec, 0.642857142)

    def test_shared_morph(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, ['x'])
        pre, rec = emma2(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.57142857)
        self.assertEqual(rec, 1)

    def test_example(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': ['koira'],
            'koiran': ['koira', 'n'],
            'koiralle': ['koira', 'lle'],
            'koirakin': ['koira', 'ki', 'n'],
            'kissa': ['ki', 'ssa'],
            'kissalle': ['kissa', 'lle'],
            'hiiri': ['hiiri']
        }
        for word, morphs in prediction.items():
            predlist.add(word, morphs)
        pre, rec = emma2(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.92857142857)
        self.assertAlmostEqual(rec, 0.85714285714)

    def test_example2(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        goldlist.add('kissassa', ['kissa', 'ssa'])
        predlist = AnalysisSet()
        prediction = {
            'koira': ['koira'],
            'koiran': ['koira', 'n'],
            'koiralle': ['koira', 'lle'],
            'koirakin': ['koira', 'ki', 'n'],
            'kissa': ['ki', 'ssa'],
            'kissalle': ['kissa', 'lle'],
            'hiiri': ['hiiri'],
            'kissassa': ['ki', 'ssa', 'ssa']
        }
        for word, morphs in prediction.items():
            predlist.add(word, morphs)
        pre, rec = emma2(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.91666666667)
        self.assertAlmostEqual(rec, 0.9375)


class TestBPR(unittest.TestCase):
    """Test the boundary precision and recall evaluation"""

    reference = {
        'koira': ['koira'],
        'koiran': ['koira', 'n'],
        'koiralle': ['koira', 'lle'],
        'koirakin': ['koira', 'kin'],
        'kissa': ['kissa'],
        'kissalle': ['kissa', 'lle'],
        'hiiri': ['hiiri']
    }

    @staticmethod
    def evaluate(*args):
        return bpr(*args)

    def test_identical(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertEqual(pre, 1)
        self.assertEqual(rec, 1)

    def test_unsegmented(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, [word])
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertEqual(pre, 1)
        self.assertAlmostEqual(rec, 0.42857142)

    def test_all_segmented(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, list(word))
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.08979591)
        self.assertEqual(rec, 1)

    def test_example(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': ['koira'],
            'koiran': ['koira', 'n'],
            'koiralle': ['koira', 'lle'],
            'koirakin': ['koira', 'ki', 'n'],
            'kissa': ['ki', 'ssa'],
            'kissalle': ['kissa', 'lle'],
            'hiiri': ['hiiri']
        }
        for word, morphs in prediction.items():
            predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.78571428)
        self.assertEqual(rec, 1.0)

    def test_example2(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        goldlist.add('kissassa', ['kissa', 'ssa'])
        predlist = AnalysisSet()
        prediction = {
            'koira': ['koira'],
            'koiran': ['koira', 'n'],
            'koiralle': ['koira', 'lle'],
            'koirakin': ['koira', 'ki', 'n'],
            'kissa': ['ki', 'ssa'],
            'kissalle': ['kissa', 'lle'],
            'hiiri': ['hiiri'],
            'kissassa': ['ki', 'ssa', 'ssa']
        }
        for word, morphs in prediction.items():
            predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.75)
        self.assertEqual(rec, 1.0)

    def test_example3(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': ['koira'],
            'koiran': ['koiran'],
            'koiralle': ['koira', 'lle'],
            'koirakin': ['koirakin'],
            'kissa': ['ki', 'ssa'],
            'kissalle': ['kissa', 'lle'],
            'hiiri': ['hiiri']
        }
        for word, morphs in prediction.items():
            predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.85714285)
        self.assertAlmostEqual(rec, 0.71428571)

    def test_example_alts1(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'koiran': [['koiran'], ['koira', 'n']],
            'koiralle': [['koiralle'], ['koira', 'lle']],
            'koirakin': [['koirakin'], ['koira', 'kin']],
            'kissa': [['kissa'], ['ki', 'ssa']],
            'kissalle': [['kissalle'], ['kissa', 'lle']],
            'hiiri': [['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 1.0)
        self.assertAlmostEqual(rec, 1.0)

    def test_example_alts2(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['k', 'o', 'i', 'r', 'a'], ['koira']],
            'koiran': [['k', 'o', 'i', 'r', 'a', 'n'], ['koira', 'n']],
            'koiralle': [['k', 'o', 'i', 'r', 'a', 'l', 'l', 'e'], ['koira', 'lle']],
            'koirakin': [['k', 'o', 'i', 'r', 'a', 'k', 'i', 'n'], ['koira', 'kin']],
            'kissa': [['k', 'i', 's', 's', 'a'], ['kissa']],
            'kissalle': [['k', 'i', 's', 's', 'a', 'l', 'l', 'e'], ['kissa', 'lle']],
            'hiiri': [['h', 'i', 'i', 'r', 'i'], ['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 1.0)
        self.assertAlmostEqual(rec, 1.0)


class TestBPRStrict(TestBPR):
    """Test the boundary precision and recall evaluation"""

    @staticmethod
    def evaluate(*args):
        return bpr_strict(*args)

    def test_example_alts1(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'koiran': [['koiran'], ['koira', 'n']],
            'koiralle': [['koiralle'], ['koira', 'lle']],
            'koirakin': [['koirakin'], ['koira', 'kin']],
            'kissa': [['kissa'], ['ki', 'ssa']],
            'kissalle': [['kissalle'], ['kissa', 'lle']],
            'hiiri': [['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, (2 + 5 * 0.5) / 7)
        self.assertAlmostEqual(rec, 1.0)

    def test_example_alts2(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['k', 'o', 'i', 'r', 'a'], ['koira']],
            'koiran': [['k', 'o', 'i', 'r', 'a', 'n'], ['koira', 'n']],
            'koiralle': [['k', 'o', 'i', 'r', 'a', 'l', 'l', 'e'], ['koira', 'lle']],
            'koirakin': [['k', 'o', 'i', 'r', 'a', 'k', 'i', 'n'], ['koira', 'kin']],
            'kissa': [['k', 'i', 's', 's', 'a'], ['kissa']],
            'kissalle': [['k', 'i', 's', 's', 'a', 'l', 'l', 'e'], ['kissa', 'lle']],
            'hiiri': [['h', 'i', 'i', 'r', 'i'], ['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.5)
        self.assertAlmostEqual(rec, 1.0)

    def test_example_alts3(self):
        goldlist = AnalysisSet()
        reference = {
            'koira': [['koira']],
            'koiran': [['koira', 'n']],
            'koiralle': [['koira', 'lle']],
            'koirakin': [['koira', 'kin'], ['koi', 'raki', 'n']],
            'kissa': [['kissa']],
            'kissalle': [['kissa', 'lle']],
            'hiiri': [['hiiri']]
        }
        for word, alts in reference.items():
            for morphs in alts:
                goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'koiran': [['koira', 'n']],
            'koiralle': [['koira', 'lle']],
            'koirakin': [['koira', 'kin']],
            'kissa': [['kissa']],
            'kissalle': [['kissa', 'lle']],
            'hiiri': [['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 1.0)
        self.assertAlmostEqual(rec, (6 + 0.5) / 7)

    def test_example_alts4(self):
        goldlist = AnalysisSet()
        reference = {
            'koira': [['koira']],
            'koiran': [['koira', 'n']],
            'koiralle': [['koira', 'lle']],
            'koirakin': [['koira', 'kin'], ['koi', 'raki', 'n']],
            'kissa': [['kissa']],
            'kissalle': [['kissa', 'lle']],
            'hiiri': [['hiiri']]
        }
        for word, alts in reference.items():
            for morphs in alts:
                goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'koiran': [['koira', 'n']],
            'koiralle': [['koira', 'lle']],
            'koirakin': [['koirakin'], ['koi', 'rakin']],
            'kissa': [['kissa']],
            'kissalle': [['kissa', 'lle']],
            'hiiri': [['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 1.0)
        self.assertAlmostEqual(rec, (6 + 0.5 * 0.5) / 7)
