import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_luotu_kassapaate_on_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukkaan_osto_toimii_kateisella(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(450)
        self.assertEqual(vaihtoraha, 50)
        self.assertEqual(self.kassapaate.maukkaat,1)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100400)

    def test_edullisen_osto_toimii_kateisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(450)
        self.assertEqual(vaihtoraha, 210)
        self.assertEqual(self.kassapaate.edulliset,1)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100240)

    def test_ei_voi_ostaa_maukasta_jos_kateinen_ei_riita(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)

    def test_ei_voi_ostaa_edullista_jos_kateinen_ei_riita(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa,100000)

    def test_maukkaan_osto_toimii_kortilla(self):
        kortti = Maksukortti(450)
        onnistuminen = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(onnistuminen, True)
        self.assertEqual(kortti.saldo, 50)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edullisen_osto_toimii_kortilla(self):
        kortti = Maksukortti(450)
        onnistuminen = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(onnistuminen, True)
        self.assertEqual(kortti.saldo, 210)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukkaan_osto_ei_onnistu_jos_kortilla_ei_ole_tarpeeksi(self):
        kortti = Maksukortti(200)
        onnistuminen = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(onnistuminen, False)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullisen_osto_ei_onnistu_jos_kortilla_ei_ole_tarpeeksi(self):
        kortti = Maksukortti(200)
        onnistuminen = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(onnistuminen, False)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kortille_lataaminen_toimii(self):
        kortti = Maksukortti(200)
        self.kassapaate.lataa_rahaa_kortille(kortti, 50)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100050)
        self.assertEqual(kortti.saldo, 250)

    def test_ei_voi_ladata_negatiivista_maaraa(self):
        kortti = Maksukortti(200)
        self.kassapaate.lataa_rahaa_kortille(kortti, -50)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kortti.saldo, 200)
    
