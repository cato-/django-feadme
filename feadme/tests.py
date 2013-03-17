from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from registration.models import RegistrationProfile
from django_hosts.reverse import reverse_full
from feadme_project import settings

def assertRedirect(testcase, response, target_url):
    testcase.assertEquals(response.status_code, 302)
    testcase.assertIn(target_url, response['Location'], 
        "the redirect target should be {expected}, but is {actual}".format(
            expected=target_url,
            actual=response['Location']
        )   
    )

class RegistrationTest(TestCase):

    def setUp(self):
        self.form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass',
            'password2': 'testpass',
        }
        self.c = Client()
        self.register_url = reverse('registration.views.register')

    def test_registration_should_redirect_to_registration_complete(self):
        """
        Test that the registration redirects to the registration complete view.
        """
        correct_redirect_url = reverse("registration_complete")

        response = self.c.post(self.register_url, self.form_data)
        assertRedirect(self, response, correct_redirect_url)

    def test_registration_should_create_registrationprofile(self):
        response = self.c.post(self.register_url, self.form_data)
        self.assertEqual(RegistrationProfile.objects.all().count(), 1)

    def test_mail_contains_activation_url(self):
        response = self.c.post(self.register_url, self.form_data)
        activation_url = reverse_full("www", "registration.views.activate", 
            view_kwargs={
            'activation_key': RegistrationProfile.objects.all()[0].activation_key
            }
        )
        print activation_url

        response = self.c.post(self.register_url, self.form_data)
        self.assertEqual(len(mail.outbox), 1)
        assert activation_url in mail.outbox[0].body
