from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json


class ApiTests(APITestCase):
    fixtures = ['test.json']

    def test_root_view_contains_link_to_documentation(self):
        url = reverse('root')
        response = self.client.get(url)
        self.assertContains(response, '/docs/', status_code=status.HTTP_200_OK)

    def test_swagger_documentation_is_visible_to_public(self):
        url = reverse('swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_all_events(self):
        url = reverse('event-list')
        response = self.client.get(url, format='json')
        self.assertContains(response, 'OPEN_SOURCED',
                            status_code=status.HTTP_200_OK)
        self.assertContains(response, 'CLOSE_SOURCED')
        self.assertContains(response, 'Matrix: Recompilations')

    def __get_remaining_seats(self, event_id):
        url = reverse('event-detail', kwargs={'pk': event_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        remaining_seats = set(
            map(int, json_response['remaining_seats'].split(', ')))
        return remaining_seats

    def test_all_seats_are_available(self):
        remaining_seats = self.__get_remaining_seats(1)
        for i in range(1, 12):
            self.assertIn(i, remaining_seats)

    def test_unreserved_seat_is_available(self):
        remaining_seats = self.__get_remaining_seats(3)
        self.assertIn(1, remaining_seats)

    def test_reserved_and_paid_seat_is_not_available(self):
        remaining_seats = self.__get_remaining_seats(3)
        self.assertNotIn(5, remaining_seats)

    def test_reserved_but_expired_seat_is_available(self):
        remaining_seats = self.__get_remaining_seats(3)
        self.assertIn(9, remaining_seats)
