from django.test import TestCase
from django.urls import reverse


class TestListaMasini(TestCase):

    def test_lista_masini_accesibila_fara_autentificare(self):
        raspuns = self.client.get(reverse('lista_masini'))

        self.assertEqual(raspuns.status_code, 200)

    
    def test_detalii_masina_inexistenta_returneaza_404(self):
        raspuns = self.client.get(
            reverse('detalii_masina', kwargs={'slug': 'masina-inexistenta'})
        )

        self.assertEqual(raspuns.status_code, 404)

    def test_lista_favorite_necesita_autentificare(self):
        raspuns = self.client.get(reverse('lista_favorite'))

        self.assertEqual(raspuns.status_code, 302)
        self.assertRedirects(
            raspuns,
            reverse('login_client') + '?next=' + reverse('lista_favorite')
        )
    def test_inregistrare_accesibila_fara_autentificare(self):
        raspuns = self.client.get(reverse('inregistrare_client'))

        self.assertEqual(raspuns.status_code, 200)
    def test_login_accesibil_fara_autentificare(self):
        raspuns = self.client.get(reverse('login_client'))

        self.assertEqual(raspuns.status_code, 200)
    def test_client_home_necesita_autentificare(self):
        raspuns = self.client.get(reverse('client_home'))

        self.assertEqual(raspuns.status_code, 302)