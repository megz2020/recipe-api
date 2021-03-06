from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email="user@test.com", password="testpass"):
    """Create sample user"""

    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        "Test creating user with email is successful"
 
        email = "admin@test.com"
        password = "Test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normlized(self):
        """Test the email for new user is normlized"""
        email="admin@TEST.COM"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")



    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'admin@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representations"""

        tag = models.Tag.objects.create(
            user = sample_user(),
            name = "Vegan"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representations"""
        
        ingred = models.Ingredient.objects.create(
            user = sample_user(),
            name = "Cucumber"

        )

        self.assertEqual(str(ingred), ingred.name)


    def test_recipe_str(self):
        """Test the recipe string representations"""
        
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            title = "Steak and mashrum souse",
            time_minutes = 5,
            price = 5.00

        )

        self.assertEqual(str(recipe), recipe.title)

