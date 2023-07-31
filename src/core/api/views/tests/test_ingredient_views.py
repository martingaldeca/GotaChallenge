import random

import factory
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status

from core.api.serializers import IngredientSerializer
from core.api.views.tests.base import APITestBase
from core.factories import IngredientFactory
from core.models import Ingredient


class IngredientListViewTest(APITestBase):
    url = reverse('core:list-ingredients')

    def test_get_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
        ingredients = [
            IngredientSerializer(
                instance=IngredientFactory(), context=self.test_context
            ).data
            for _ in range(random.randint(1, 5))
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], ingredients)

    def test_filter_by_vegetarian_200_OK(self):
        ingredients = [
            IngredientSerializer(
                instance=IngredientFactory(
                    food_type=Ingredient.VEGETARIAN_FOOD_TYPES[0]
                ),
                context=self.test_context,
            ).data
            for _ in range(random.randint(1, 5))
        ]
        IngredientFactory(food_type=Ingredient.T_MEAT)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(ingredients) + 1)

        response = self.client.get(self.url, {'vegetarian': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], ingredients)

    def test_filter_by_vegan_200_OK(self):
        ingredients = [
            IngredientSerializer(
                instance=IngredientFactory(
                    food_type=Ingredient.VEGAN_FOOD_TYPES[0]
                ),
                context=self.test_context,
            ).data
            for _ in range(random.randint(1, 5))
        ]
        IngredientFactory(food_type=Ingredient.T_MEAT)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(ingredients) + 1)

        response = self.client.get(self.url, {'vegan': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], ingredients)


class CreateNewIngredientViewTest(APITestBase):
    url = reverse('core:create-ingredient')

    def test_create_new_ingredient_201_CREATED(self):
        ingredient_name = 'test_name'
        ingredient_description = 'test_description'
        ingredient_food_type = Ingredient.VEGAN_FOOD_TYPES[0]
        ingredient_calories = random.uniform(0.01, 2500)
        ingredient_price = random.uniform(0.01, 2500)
        ingredient_image = ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
        data_to_send = {
            'name': ingredient_name,
            'description': ingredient_description,
            'food_type': ingredient_food_type,
            'calories': ingredient_calories,
            'price': ingredient_price,
            'image': ingredient_image,
        }
        self.assertEqual(Ingredient.objects.count(), 0)
        response = self.client.post(self.url, data=data_to_send)
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ingredient = Ingredient.objects.last()
        self.assertEqual(
            response.data,
            IngredientSerializer(
                instance=ingredient,
                context=self.test_context
            ).data
        )
        self.assertEqual(ingredient.name, ingredient_name)
        self.assertEqual(ingredient.description, ingredient_description)


class RetrieveUpdateDestroyIngredientViewTest(APITestBase):
    url = reverse('core:ingredient', kwargs={'uuid': None})

    def test_get_ingredient_200_OK(self):
        ingredient: Ingredient = IngredientFactory()
        self.url = reverse('core:ingredient', kwargs={'uuid': ingredient.uuid.hex})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, IngredientSerializer(instance=ingredient, context=self.test_context).data)

    def test_update_ingredient_200_OK(self):
        ingredient: Ingredient = IngredientFactory()
        self.url = reverse('core:ingredient', kwargs={'uuid': ingredient.uuid.hex})

        new_name = 'test_name_2'
        new_description = 'test_description_2'
        new_food_type = Ingredient.VEGAN_FOOD_TYPES[0]
        new_calories = 1994.0
        new_price = 1994.0
        new_image = ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
        data = {
            'name': new_name,
            'description': new_description,
            'food_type': new_food_type,
            'calories': new_calories,
            'price': new_price,
            'image': new_image,
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(
            response.data,
            IngredientSerializer(
                instance=ingredient,
                context=self.test_context
            ).data
        )
        self.assertEqual(ingredient.name, new_name)
        self.assertEqual(ingredient.description, new_description)
        self.assertEqual(ingredient.food_type, new_food_type)
        self.assertEqual(ingredient.calories, new_calories)
        self.assertEqual(ingredient.price, new_price)
        self.assertSameFile(ingredient.image, new_image)

    def test_delete_ingredient_204_NO_CONTENT(self):
        ingredient: Ingredient = IngredientFactory()
        self.assertEqual(Ingredient.objects.count(), 1)
        self.url = reverse('core:ingredient', kwargs={'uuid': ingredient.uuid.hex})
        response = self.client.delete(self.url)
        self.assertEqual(Ingredient.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
