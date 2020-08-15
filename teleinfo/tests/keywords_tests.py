import unittest

from models.Keywords import Keyword


class KeywordsTests(unittest.TestCase):
    def test_name(self):
        self.assertEqual("HCHP", Keyword.HCHP.name())
        self.assertEqual("HCHC", Keyword.HCHC.name())
        self.assertEqual("IINST", Keyword.IINST.name())
        self.assertEqual("ISOUSC", Keyword.ISOUSC.name())
        self.assertEqual("OPTARIF", Keyword.OPTARIF.name())
        self.assertEqual("PAPP", Keyword.PAPP.name())
        self.assertEqual("BBR_HP_JB", Keyword.BBR_HP_JB.name())

    def test_is_int_value(self):
        self.assertTrue(Keyword.HCHC.is_int_value())
        self.assertTrue(Keyword.HCHP.is_int_value())
        self.assertTrue(Keyword.IINST.is_int_value())
        self.assertTrue(Keyword.PAPP.is_int_value())
        self.assertTrue(Keyword.ISOUSC.is_int_value())
        self.assertTrue(Keyword.ADCO.is_int_value())

    def test_is_unsuported_keyword(self):
        self.assertTrue(Keyword.BBR_HC_JW.is_unsupported_keyword())
        self.assertTrue(Keyword.BBR_HP_JR.is_unsupported_keyword())
        self.assertTrue(Keyword.EJP_HPM.is_unsupported_keyword())

        self.assertFalse(Keyword.IINST.is_unsupported_keyword())
        self.assertFalse(Keyword.HCHP.is_unsupported_keyword())
        self.assertFalse(Keyword.HHPHC.is_unsupported_keyword())
        self.assertFalse(Keyword.MOTDETAT.is_unsupported_keyword())
        self.assertFalse(Keyword.ADCO.is_unsupported_keyword())

    def test_value_of(self):
        self.assertEqual(Keyword.HCHP, Keyword.value_of("HCHP"))
        self.assertEqual(Keyword.IINST, Keyword.value_of("IINST"))
        self.assertEqual(Keyword.OPTARIF, Keyword.value_of("OPTARIF"))
        self.assertEqual(Keyword.PAPP, Keyword.value_of("PAPP"))

        with self.assertRaises(Exception):
            Keyword.value_of("EJP_HPM")
