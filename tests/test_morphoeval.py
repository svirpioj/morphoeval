"""Unit tests for morphoeval"""

import unittest

from morphoeval import *


class TestCoMMA(unittest.TestCase):
    """Test CoMMA method"""

    @staticmethod
    def evaluate(*args, **kwargs):
        return comma(*args, **kwargs)

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
        self.assertEqual(rec, 0)

    def test_unsegmented_diag(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, [word])
        pre, rec = self.evaluate(goldlist, predlist, diagonals=True)
        self.assertEqual(pre, 1)
        self.assertAlmostEqual(rec, 11 / 30)

    def test_shared_morph(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, ['x'])
        pre, rec = self.evaluate(goldlist, predlist)
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
        pre, rec = self.evaluate(goldlist, predlist)
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
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.70238095)
        self.assertAlmostEqual(rec, 0.76190476)

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
        self.assertEqual(pre, 1.0)
        self.assertEqual(rec, 1.0)

    def test_example_alts2(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['x'], ['koira']],
            'koiran': [['x'], ['koira', 'n']],
            'koiralle': [['x'], ['koira', 'lle']],
            'koirakin': [['x'], ['koira', 'kin']],
            'kissa': [['x'], ['kissa']],
            'kissalle': [['x'], ['kissa', 'lle']],
            'hiiri': [['x'], ['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.25612244)
        self.assertEqual(rec, 1.0)

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
        # no co-occurrences for "hiiri", 3/4 points for "koiran" and "koirakin", full for the rest
        self.assertAlmostEqual(rec, (4 + 2 * 0.75) / 6)

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
        # 2/3 for "koira" (missing one hit to "koirakin")
        # 2/4 for "koiran" (missing two hits to "koirakin")
        # 3/4 for "koiralle" (missing one hit to "koirakin")
        # zero for "koirakin"
        # 1 for "kissa", "kissalle"
        # no co-occurrences for "hiiri"
        self.assertAlmostEqual(rec, (2/3 + 0.5 + 0.75 + 2 * 1) / 6)


class TestCoMMAS(TestCoMMA):
    """Test CoMMA-S method"""

    @staticmethod
    def evaluate(*args, **kwargs):
        return comma_strict(*args, **kwargs)

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
        # no co-occurrences for "kissa", one point for "koira", half for others
        self.assertAlmostEqual(pre, (1 + 0.5 * 5) / 6)
        self.assertEqual(rec, 1.0)

    def test_example_alts2(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['x'], ['koira']],
            'koiran': [['x'], ['koira', 'n']],
            'koiralle': [['x'], ['koira', 'lle']],
            'koirakin': [['x'], ['koira', 'kin']],
            'kissa': [['x'], ['kissa']],
            'kissalle': [['x'], ['kissa', 'lle']],
            'hiiri': [['x'], ['hiiri']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        # no points for "hiiri", half points for others
        self.assertAlmostEqual(pre, (0.5 * 6) / 7)
        self.assertEqual(rec, 1.0)

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
        # no co-occurrences for "hiiri", half points for "koirakin", full for the rest
        self.assertAlmostEqual(rec, (5 + 0.5) / 6)

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
        # 2/3 for "koira", "koiran" (missing "koirakin")
        # 3/4 for "koiralle" (missing "koirakin")
        # zero for "koirakin"
        # 1 for "kissa", "kissalle"
        # no co-occurrences for "hiiri"
        self.assertAlmostEqual(rec, (2 * 2/3 + 3/4 + 2 * 1) / 6)


class TestEMMA2(unittest.TestCase):
    """Test EMMA-2 method"""

    @staticmethod
    def evaluate(*args, **kwargs):
        return emma2(*args, **kwargs)

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
        # 1 for "koira", "kissa", "hiiri"
        # 0.5 for "koiran", "koiralle", "koirakin"
        # 0 for "kissalle"
        self.assertAlmostEqual(rec, (3 + 3 * 0.5) / 7)
        self.assertEqual(pre, 1)

    def test_shared_morph(self):
        goldlist = AnalysisSet()
        for word, morphs in self.reference.items():
            goldlist.add(word, morphs)
        predlist = AnalysisSet()
        for word, morphs in self.reference.items():
            predlist.add(word, ['x'])
        pre, rec = self.evaluate(goldlist, predlist)
        # "x" mapped to "koira"; first 4 words have a real shared morph
        self.assertAlmostEqual(pre, 4 / 7)
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
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertAlmostEqual(pre, 0.91666666667)
        self.assertAlmostEqual(rec, 0.9375)

    def test_example_alts_1(self):
        goldlist = AnalysisSet()
        reference = {
            'koira': [['koira']],
            'kissa': [['kissa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
        }
        for word, alts in reference.items():
            for morphs in alts:
                goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'kissa': [['kissa'], ['ki', 'ssa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        # "ki" and "ssa" are unique -> full points
        self.assertEqual(pre, 1.0)
        self.assertEqual(rec, 1.0)

    def test_example_alts_2(self):
        goldlist = AnalysisSet()
        reference = {
            'koira': [['koira']],
            'kissa': [['kissa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'puussa': [['puu', 'ssa']]
        }
        for word, alts in reference.items():
            for morphs in alts:
                goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'kissa': [['kissa'], ['ki', 'ssa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'puussa': [['puu', 'ssa']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        # pred incorrectly shares "ssa" between "kissa" and "puussa"
        # - "kissa" mapped to "kissa", "ki", and "ssa"
        # - full points for "koira", "koiran" ,"kissa"
        # - 2/4 points for "kissan"
        self.assertAlmostEqual(pre, (4 + 0.5) / 5)
        self.assertEqual(rec, 1.0)

    def test_example_alts_2(self):
        goldlist = AnalysisSet()
        reference = {
            'koira': [['koira']],
            'kissa': [['kissa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'puussa': [['puu', 'ssa']]
        }
        for word, alts in reference.items():
            for morphs in alts:
                goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'kissa': [['kissa'], ['ki', 'ssa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'puussa': [['puu', 'ssa']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        # pred incorrectly shares "ssa" between "kissa" and "puussa"
        # - "kissa" mapped to "kissa", "ki", and "ssa"
        # - full points for "koira", "koiran" ,"kissa"
        # - 2/4 points for "kissan"
        self.assertAlmostEqual(pre, (4 + 0.5) / 5)
        self.assertEqual(rec, 1.0)

    def test_example_alts_3(self):
        goldlist = AnalysisSet()
        reference = {
            'koira': [['koira']],
            'kissa': [['kissa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'koirakin': [['koira', 'kin'], ['koi', 'raki', 'n']]
        }
        for word, alts in reference.items():
            for morphs in alts:
                goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'kissa': [['kissa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'koirakin': [['koira', 'kin']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertEqual(pre, 1.0)
        # - "koira" mapped to "koira", "koi", and "raki"
        # - full points for "koira", "kissa", "koiran", "koirakin"
        # - 1/2 points for "kissan" (no shared n)
        self.assertAlmostEqual(rec, (4 + 0.5) / 5)

    def test_example_alts_4(self):
        goldlist = AnalysisSet()
        reference = {
            'koira': [['koira']],
            'kissa': [['kissa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'koirakin': [['koira', 'kin'], ['koi', 'raki', 'n']],
            'koin': [['koi', 'n']]
        }
        for word, alts in reference.items():
            for morphs in alts:
                goldlist.add(word, morphs)
        predlist = AnalysisSet()
        prediction = {
            'koira': [['koira']],
            'kissa': [['kissa']],
            'koiran': [['koira', 'n']],
            'kissan': [['kissa', 'n']],
            'koirakin': [['koira', 'kin'], ['koiraki', 'n']],
            'koin': [['koin']]
        }
        for word, alts in prediction.items():
            for morphs in alts:
                predlist.add(word, morphs)
        pre, rec = self.evaluate(goldlist, predlist)
        self.assertEqual(pre, 1.0)
        # - "koira" mapped to "koira", "kin", "koi", "raki"
        # - no points for "koin"
        # - full points for others
        self.assertEqual(rec, 5 / 6)


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
