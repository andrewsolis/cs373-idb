#!/usr/bin/env python3

#import unittest
from django.test import TestCase
from django.utils import unittest
from django.test.client import RequestFactory

from idb.videogames.models import *
from django.http import HttpResponse, HttpRequest

from json import dumps
from ast import literal_eval
from idb.api.views import *

base_company_input = { "mapimage": "http:/map.com", "description": "description", "webpage": "http://company.com/", "founded": "1889-01-01T00:00:00Z", "location": "TX", "images": ["http://image.com"], "name": "Company" }
base_company = base_company_input.copy()
base_company.pop("images")
updated_company_input = { "mapimage": "http:/map2.com", "description": "description2", "webpage": "http://company2.com/", "founded": "2001-01-01T00:00:00Z", "location": "TX2", "images": ["http://image2.com"], "name": "Company2" }
updated_company = updated_company_input.copy()
updated_company.pop("images")

base_person_input = {"name": "person", "videos": ["http://video.com"], "DOB": "1959-07-23T00:00:00Z", "residence": "TX", "twitter": "twitter", "companies": [1], "images": ["http://image.com"], "description": "description"}
base_person = base_person_input.copy()
base_person.pop("images")
base_person.pop("videos")
base_person_companies = base_person.pop("companies")

base_game_input = {"name": "Metroid", "images": ["http://upload.wikimedia.org/wikipedia/en/5/5d/Metroid_boxart.jpg"], "people": [1], "release_date": "1986-08-06T00:00:00Z", "system": "NES", "copies": 273000, "gamefaq": "http://www.gamefaqs.com/nes/519689-metroid", "synopsis": "description for metroid", "videos": ["www.youtube.com/embed/WT4pW6n7-rg"], "genre": ["Side Scroller"], "company": 1}

base_system = {"platform" : "NES"}
base_genre = {"types" : "Side Scroller"}

base_game = {"name": "Metroid", "release_date": "1986-08-06T00:00:00Z", "copies": 273000, "gamefaq": "http://www.gamefaqs.com/nes/519689-metroid", "synopsis": "description for metroid", "system": System.objects.get(pk=1), "company": Company.objects.get(pk=1)}
base_game_people = [1]
base_game_company = 1
base_game_system = 1
base_game_genre = [1]



id_1 = {"id": 1}
id_2 = {"id": 2}

# --------
# Test API
# --------

class TestGames (TestCase):
    pass

class TestPeople (TestCase):
    pass

class TestCompany (TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_POST_company(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        response_content = literal_eval(response.content.decode('utf-8'))
        db_query = literal_eval(serializers.serialize("json",[Company.objects.get(pk = 1)]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content, id_1)
        self.assertEqual(db_query[0]["fields"], base_company)

    def test_POST_company_with_no_image_key(self):
        request = self.factory.post('api/companies/', base_company, content_type='application/json')
        response = api_companies(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_company_with_empty_image(self):
        company_data = base_company_input.copy()
        company_data["images"] = []
        request = self.factory.post('api/companies/', company_data, content_type='application/json')
        response = api_companies(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_company_with_no_name(self):
        company_data = base_company_input.copy()
        company_data.pop("name")
        request = self.factory.post('api/companies/', company_data, content_type='application/json')
        response = api_companies(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_company_with_empty_name(self):
        company_data = base_company_input.copy()
        company_data["name"] = " "
        request = self.factory.post('api/companies/', company_data, content_type='application/json')
        response = api_companies(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_GET_all_companies(self):
        new_company = Company(**base_company).save()
        new_company = Company(**base_company).save()
        request = self.factory.get('api/companies/')
        response = api_companies(request)
        response_content = response.content.decode('utf-8')
        db_query = serializers.serialize("json",Company.objects.all(), fields=("name"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db_query, response_content)

    def test_PUT_company(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        request = self.factory.put('api/companies/1/', updated_company_input, content_type='application/json')
        response = api_companies_id(request, '1')
        response_content = response.content.decode('utf-8')
        company_object = Company.objects.get(pk=1)
        db_query = literal_eval(serializers.serialize("json",[company_object]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(db_query[0]["fields"], updated_company)
        self.assertEqual(company_object.images()[0].link, updated_company_input["images"][0])

    def test_PUT_company_with_bad_id(self):
        request = self.factory.put('api/companies/1/', updated_company_input, content_type='application/json')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_PUT_company_with_no_image_key(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        request = self.factory.put('api/companies/1/', updated_company, content_type='application/json')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_company_with_empty_image(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        company_data = base_company_input.copy()
        company_data["images"] = []
        request = self.factory.put('api/companies/1/', company_data, content_type='application/json')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_company_with_no_name(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        company_data = base_company_input.copy()
        company_data.pop("name")
        request = self.factory.put('api/companies/1/', company_data, content_type='application/json')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_company_with_empty_name(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        company_data = base_company_input.copy()
        company_data["name"] = " "
        request = self.factory.put('api/companies/1/', company_data, content_type='application/json')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_GET_company(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        request = self.factory.get('api/companies/1/')
        response = api_companies_id(request, '1')
        company_object = Company.objects.get(pk=1)
        db_query = literal_eval(serializers.serialize("json",[company_object]))
        response_content = literal_eval(response.content.decode('utf-8'))
        image_link = response_content[0]["fields"].pop("images")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db_query, response_content)
        self.assertEqual(company_object.images()[0].link, image_link[0])

    def test_GET_with_bad_id(self):
        request = self.factory.get('api/companies/1/')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_DELETE_company(self):
        request = self.factory.post('api/companies/', base_company_input, content_type='application/json')
        response = api_companies(request)
        request = self.factory.delete('api/companies/1/')
        response = api_companies_id(request, '1')
        self.assertEqual(len(Images.objects.filter(other_id = 1, other_type = 'CP')), 0)
        self.assertEqual(len(Company.objects.filter(pk = 1)), 0)
        self.assertEqual(response.status_code, 204)

    def test_DELETE_with_bad_id(self):
        request = self.factory.delete('api/companies/1/')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_intersection_company_games(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        System(**base_system).save()
        Genre(**base_genre).save()
        new_game = Game(**base_game)
        new_game.save()
        new_game.genre.add(1)
        new_game.people.add(1)
        request = self.factory.get('api/companies/1/games/')
        response = api_companies_games(request, 1)
        response_content = response.content.decode('utf-8')
        db_query = serializers.serialize("json", Game.objects.filter(company = 1), fields=("name"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content, db_query)

    def test_GET_intersection_company_games_with_bad_id(self):
        request = self.factory.get('api/companies/1/games/')
        response = api_companies_games(request, '1')
        # print(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_intersection_company_people(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        request = self.factory.get('api/companies/1/people/')
        response = api_companies_people(request, 1)
        response_content = response.content.decode('utf-8')
        db_query = serializers.serialize("json", Person.objects.filter(companies = 1), fields=("name"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content, db_query)

    def test_GET_intersection_company_people_with_bad_id(self):
        request = self.factory.get('api/companies/1/people/')
        response = api_companies_people(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

print("tests.py")
print("Done.")