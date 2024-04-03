from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from first_lab.models import BookLover


# Create your tests here.
class BookLoverViewSetByIdTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_lover = BookLover.objects.create(
            first_name='John',
            last_name='Doe',
            middle_name='Smith',
            birthday='1990-01-01',
            date_of_joining='2022-01-01',
            address='123 Main St',
            phone='555-1234'
        )

    def test_get_book_lover(self):
        response = self.client.get(f'/your-api-endpoint/{self.book_lover.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book_lover(self):
        updated_data = {
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        response = self.client.put(f'/your-api-endpoint/{self.book_lover.pk}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookLover.objects.get(pk=self.book_lover.pk).first_name, updated_data['first_name'])
        self.assertEqual(BookLover.objects.get(pk=self.book_lover.pk).last_name, updated_data['last_name'])

    def test_delete_book_lover(self):
        response = self.client.delete(f'/your-api-endpoint/{self.book_lover.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
