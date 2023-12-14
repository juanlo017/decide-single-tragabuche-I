from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_identity_neg(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected_result)

    def test_paridad(self):
        data = {
            'type': 'PARIDAD',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 6 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        # Calcula la suma total de votos
        total_votes = sum(opt['votes'] for opt in data['options'])

        # Ahora, esperamos que el postprocesamiento de paridad ajuste los votos proporcionalmente
        expected_result = [
            { 'option': 'Option 5', 'number': 5, 'votes': 6, 'postproc': int(6 / total_votes * total_votes) },
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': int(5 / total_votes * total_votes) },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': int(3 / total_votes * total_votes) },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': int(2 / total_votes * total_votes) },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': int(1 / total_votes * total_votes) },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': int(0 / total_votes * total_votes) },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_paridad_1(self):
        data = {
            'type': 'PARIDAD',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 6 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }
        expected_result = [
            { 'option': 'Option 5', 'number': 5, 'votes': 6, 'postproc': 6 },
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_paridad_2(self):
        data = {
            'type': 'PARIDAD',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 6 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        # Calcula la suma total de votos

        # Ahora, esperamos que el postprocesamiento de paridad ajuste los votos proporcionales
        expected_result = [
            { 'option': 'Option 5', 'number': 5, 'votes': 6, 'postproc': 6 },
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_paridad_caso_3(self):
        data = {
            'type': 'PARIDAD',
            'options': []
        }
        expected_result = []

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)
        values = response.json()
        self.assertEqual(values, expected_result)

    def test_paridad_neg(self):
        data = {
            'type': 'PARIDAD',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 6 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        # Calcula la suma total de votos
        total_votes = sum(opt['votes'] for opt in data['options'])

        # Ahora, esperamos que el postprocesamiento de paridad ajuste los votos proporcionalmente
        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': int(5 / total_votes * total_votes) },
            { 'option': 'Option 5', 'number': 5, 'votes': 6, 'postproc': int(6 / total_votes * total_votes) },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': int(3 / total_votes * total_votes) },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': int(2 / total_votes * total_votes) },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': int(1 / total_votes * total_votes) },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': int(0 / total_votes * total_votes) },
        ]

        response = self.client.post('/postproc/', data, format='json')

        values = response.json()
        self.assertNotEqual(values, expected_result)

    def test_borda_count_standard(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'name': 'Option A', 'votes': 10}, 
                {'name': 'Option B', 'votes': 5}
            ]
        }
        
        expected_output = [
            {'name': 'Option A', 'votes': 10, 'postproc': 20}, 
            {'name': 'Option B', 'votes': 5, 'postproc': 5}
        ]

        response = self.client.post('/postproc/', data, format='json')

        values = response.json()

        self.assertEqual(values, expected_output)

    def test_borda_count_single_option(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'name': 'Option A', 'votes': 100}
            ]
        }
        expected_output = [{'name': 'Option A', 'votes': 100, 'postproc': 100}]

        response = self.client.post('/postproc/', data, format='json')
        values = response.json()

        self.assertEqual(values, expected_output)


    def test_borda_count_empty(self):
        data = {
            'type': 'BORDA',
            'options': []
        }
        expected_output = []
        
        response = self.client.post('/postproc/', data, format='json')
        values = response.json()

        self.assertEqual(values, expected_output)
