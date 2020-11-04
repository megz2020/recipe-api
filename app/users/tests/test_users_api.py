from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
USER_MANAGE_URL = reverse('users:manage')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicApiTests(TestCase):
    """Test user API [public]"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload"""

        payload = {
            'email': 'admin@test.com',
            'password': 'testpass',
            'name': 'Test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):

        """ Test creating user that already exists fails"""

        payload = {
            'email': 'admin@test.com',
            'password': 'testpass',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test the password must complex"""

        payload = {
            'email': 'admin@test.com',
            'password': 'pw',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        "Test if token is created for user"

        payload = {'email': 'admin@test.com', 'password': 'testpass'}

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created when credentials are invalid"""
        create_user(email="admin@test.com", password="testpass")
        payload = {'email': "fake@test.com", "password": "fakepass"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created when user not exits"""

        payload = {'email': "test@test.com", "password": "testpass"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are requierd """

        payload = {'email': "test@test.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reterive_user_unauthorized(self):
        """Test that authenticate is required for users management"""

        res = self.client.get(USER_MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApi(TestCase):
    """Test API that require auth"""

    def setUp(self):
        payload = {
            'email': 'admin@test.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        self.user = create_user(**payload)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profiel_success(self):
        """Test retrieveing profile for logged in used"""
        res = self.client.get(USER_MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed(self):
        """Test that POST is not allwed on this url"""
        res = self.client.post(USER_MANAGE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(USER_MANAGE_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
