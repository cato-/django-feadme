import re
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
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


def assertRedirectToLoginPage(testcase, response):
    assertRedirect(testcase, response, reverse("django.contrib.auth.views.login"))


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

        response = self.c.post(self.register_url, self.form_data)
        self.assertEqual(len(mail.outbox), 1)
        assert activation_url in mail.outbox[0].body


class EditProfileFormTests(TestCase):

    fixtures = ['adminuser.json']

    def setUp(self):
        self.c = Client()
        self.c.login(username="admin", password="admin")
        self.profile_edit_url = reverse("profile_edit")
        # data like the adminuser in the fixture
        self.post_data = {
            'username': 'admin',
            'email': 'admin@fead.me',
            'first_name': '',
            'last_name': '',
            'date_joined': '2013-03-16 15:04:01'
        }

    def assert_success_message(self, response):
        self.assertContains(response, "Profile saved")

    def test_page_needs_login(self):
        self.c.logout()
        response = self.c.get(self.profile_edit_url)
        assertRedirectToLoginPage(self, response)

    def test_form_does_not_contain_internal_fields(self):
        response = self.c.get(self.profile_edit_url)
        self.assertNotContains(response, "id_is_superuser")

    def test_username_field_is_marked_readonly(self):
        response = self.c.get(self.profile_edit_url)
        # not the ideal solution
        re.match(r'id_username.*readonly', response.content)

    def test_cannot_change_readonly_username(self):
        user = User.objects.get(id=1)  # see fixture
        self.assertEqual(user.username, "admin")
        self.post_data['username'] = 'changed_username'
        response = self.c.post(self.profile_edit_url, self.post_data)
        self.assert_success_message(response)
        changed_user = User.objects.get(id=1)  # see fixture
        self.assertEqual(changed_user.username, "admin")

    def test_can_change_first_name(self):
        user = User.objects.get(id=1)  # see fixture
        self.assertEqual(user.first_name, "")
        self.post_data['first_name'] = 'Simon'
        response = self.c.post(self.profile_edit_url, self.post_data)
        self.assert_success_message(response)
        changed_user = User.objects.get(id=1)  # see fixture
        self.assertEqual(changed_user.first_name, "Simon")
