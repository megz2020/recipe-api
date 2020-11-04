from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly avaliable ingred API""" 

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    

class PrivateIngredientsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com",
            "testpass"
        )

        self.client.force_authenticate(self.user)

        def test_reterive_ingredient_list(self):

            Ingredient.objects.create(user=self.user, name="onian")
            Ingredient.objects.create(user=self.user, name="salt")

            res = self.client.get(INGREDIENTS_URL)
            ingredients = Ingredient.objects.all().order_by('--name')
            serializer = IngredientSerializer(ingredients, many=True)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)


        def test_ingredients_limited_to_user(self):

            user2 = get_user_model().objects.create_user(
                "user2@test.com",
                "testpass"
            )

            Ingredient.objects.create(
                user=user2,
                name="vegt"
            )

            ingredient = Ingredient.objects.create(
                user=self.user,
                name="salt"
            )

            res = self.client.get(INGREDIENTS_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data), 1)
            self.assertEqual(res.data[0]["name"], ingredient.name)

