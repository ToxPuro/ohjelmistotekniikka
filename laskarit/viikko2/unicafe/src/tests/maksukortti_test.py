import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(600)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 6.0")

    def test_lataaminen_lisaa_saldoa(self):
        self.maksukortti.lataa_rahaa(10)
        self.assertEqual(str(self.maksukortti), "saldo: 6.1")

    ## en ole varma onko tämä haluttu testi, mutta oletan että pitäisi olla, eihän kaikki testit aina mene läpi
    def test_negatiivinen_lataaminen_ei_muuta_saldo(self):
        self.maksukortti.lataa_rahaa(-10)
        self.assertEqual(str(self.maksukortti), "saldo: 6.0")

    def test_ei_voi_ottaa_liikaa(self):
        onnistuminen = self.maksukortti.ota_rahaa(700)
        self.assertEqual(onnistuminen, False)
        self.assertEqual(str(self.maksukortti), "saldo: 6.0")

    def test_voi_ottaa_rahaa(self):
        onnistuminen = self.maksukortti.ota_rahaa(500)
        self.assertEqual(onnistuminen, True)
        self.assertEqual(str(self.maksukortti), "saldo: 1.0")

    
