#!/usr/bin/env python3

#import unittest
from django.test import TestCase
from django.utils import unittest
from django.test.client import RequestFactory

from idb.videogames.models import *
from idb.search import *
from django.http import HttpResponse, HttpRequest

from json import dumps
from ast import literal_eval
from idb.api.views import *

base_company_input = {"mapimage": "http:/map.com", "description": "description", "twitter" : "twitter", "webpage": "http://company.com/", "founded": "1889-01-01T00:00:00Z", "location": "TX", "images": ["http://image.com"], "name": "Company"}
base_company = base_company_input.copy()
base_company.pop("images")
updated_company_input = {"mapimage": "http:/map2.com", "description": "description2", "twitter" : "twitter", "webpage": "http://company2.com/", "founded": "2001-01-01T00:00:00Z", "location": "TX2", "images": ["http://image2.com"], "name": "Company2"}
updated_company = updated_company_input.copy()
updated_company.pop("images")

base_person_input =    {"name": "person", "videos": ["http://video.com"], "DOB": "1959-07-23T00:00:00Z", "residence": "TX", "twitter": "twitter", "companies": [1], "images": ["http://image.com"], "description": "description"}
updated_person_input = {"name": "person2", "videos": ["http://video2.com"], "DOB": "2010-07-23T00:00:00Z", "residence": "TX2", "twitter": "twitter2", "companies": [1], "images": ["http://image2.com"], "description": "description2"}
updated_person = updated_person_input.copy()
updated_person.pop("images")
updated_person.pop("videos")

base_person = base_person_input.copy()
base_person.pop("images")
base_person.pop("videos")
base_person_post = base_person.copy() 
base_person_companies = base_person.pop("companies")

base_system = {"platform" : "NES"}
base_genre = {"types" : "Side Scroller"}

base_game_input = {"name": "game", "images": ["http://image.com"], "people": [1], "release_date": "1986-08-06T00:00:00Z", "system": "NES", "copies": 273000, "gamefaq": "http://www.gamefaqs.com", "synopsis": "description", "videos": ["www.video.com"], "genre": ["Side Scroller"], "company": 1}
base_game = {"name": "game", "release_date": "1986-08-06T00:00:00Z", "copies": 273000, "gamefaq": "http://www.gamefaqs.com", "synopsis": "description", "system": System.objects.get(pk=1), "company": Company.objects.get(pk=1)}
base_game_people = [1]
base_game_genre = [1]
base_game_output = {"name": "game", "release_date": "1986-08-06T00:00:00Z", "copies": 273000, "gamefaq": "http://www.gamefaqs.com", "synopsis": "description", "system": 1, "company": 1, "people": [1], "genre": [1]}
updated_game_input = {"name": "game2", "images": ["http://image2.com"], "people": [1], "release_date": "2000-08-06T00:00:00Z", "system": "NES", "copies": 273000, "gamefaq": "http://www.gamefaqs2.com", "synopsis": "description2", "videos": ["www.video2.com"], "genre": ["Side Scroller"], "company": 1}
updated_game = updated_game_input.copy()
updated_game.pop("images")
updated_game.pop("videos")
updated_game["system"] = 1
updated_game["genre"] = [1]

id_1 = {"id": 1}

def setup_db_for_game():
    new_company = Company(**base_company).save()
    new_person = Person(**base_person)
    new_person.save()
    new_person.companies.add(1)
    System(**base_system).save()
    Genre(**base_genre).save()

# --------
# Test API
# --------

class TestGames (TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_POST_game(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        response_content = literal_eval(response.content.decode('utf-8'))
        db_query = literal_eval(serializers.serialize("json",[Game.objects.get(pk = 1)]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content, id_1)
        self.assertEqual(db_query[0]["fields"], base_game_output)

    def test_POST_game_with_no_image_key(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data.pop("images")
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_empty_image(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["images"] = []
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_no_name(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data.pop("name")
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_empty_name(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["name"] = " "
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_no_video(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data.pop("videos")
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_empty_video(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["videos"] = []
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_no_company(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data.pop("company")
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_empty_company(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["company"] = None
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_invalid_company(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["company"] = 2
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_no_people(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data.pop("people")
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_empty_people(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["people"] = []
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_invalid_people(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["people"] = [2]
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_no_genre(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data.pop("genre")
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_empty_genre(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["genre"] = []
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_invalid_genre(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["genre"] = [2]
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_no_system(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data.pop("system")
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_empty_system(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["system"] = None
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_game_with_invalid_system(self):
        setup_db_for_game()
        game_data = base_game_input.copy()
        game_data["system"] = 3
        request = self.factory.post('api/games/', game_data, content_type='application/json')
        response = api_games(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_all_games(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.get('api/games/')
        response = api_games(request)
        response_content = literal_eval(response.content.decode('utf-8'))
        db_query = literal_eval(serializers.serialize("json", Game.objects.all(), fields=("name")))
        db_query[0]["fields"]["images"] = ["http://image.com"]
        db_query[1]["fields"]["images"] = ["http://image.com"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db_query, response_content)

    def test_PUT_game(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.put('api/games/1/', updated_game_input, content_type='application/json')
        response = api_games_id(request, 1)
        response_content = response.content.decode('utf-8')
        game_object = Game.objects.get(pk=1)
        db_query = literal_eval(serializers.serialize("json",[game_object]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(db_query[0]["fields"], updated_game)
        self.assertEqual(game_object.images()[0].link, updated_game_input["images"][0])
        self.assertEqual(game_object.videos()[0].link, updated_game_input["videos"][0])

    def test_PUT_game_with_empty_image(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["images"] = []
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_empty_name(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["name"] = []
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_empty_video(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["videos"] = []
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_empty_company(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["company"] = None
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_invalid_company(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["company"] = 2
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_empty_people(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["people"] = []
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_invalid_people(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["people"] = [2]
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_empty_genre(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["genre"] = []
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_invalid_genre(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["people"] = [2]
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_empty_system(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["system"] = None
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_game_with_invalid_system(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        game_data = base_game_input.copy()
        game_data["system"] = "mitch"
        request = self.factory.put('api/games/1/', game_data, content_type='application/json')
        response = api_games_id(request, 1)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_game(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.get('api/games/1/')
        response = api_games_id(request, '1')
        game_object = Game.objects.get(pk=1)
        db_query = literal_eval(serializers.serialize("json",[game_object]))
        response_content = literal_eval(response.content.decode('utf-8'))
        image_list = response_content[0]["fields"].pop("images")
        video_list = response_content[0]["fields"].pop("videos")
        response_content[0]["fields"]["genre"] = [1]
        response_content[0]["fields"]["system"] = 1
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db_query, response_content)
        self.assertEqual(game_object.images()[0].link, image_list[0])
        self.assertEqual(game_object.videos()[0].link, video_list[0])

    def test_GET_game_with_bad_id(self):
        request = self.factory.get('api/games/1/')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_DELETE_games(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.delete('api/games/1/')
        response = api_games_id(request, '1')
        self.assertEqual(len(Images.objects.filter(other_id = 1, other_type = 'GM')), 0)
        self.assertEqual(len(Images.objects.filter(other_id = 1, other_type = 'GM')), 0)
        self.assertEqual(len(Game.objects.filter(pk = 1)), 0)
        self.assertEqual(response.status_code, 204)

    def test_DELETE_game_with_bad_id(self):
        request = self.factory.delete('api/games/1/')
        response = api_companies_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_intersection_games_people(self):
        setup_db_for_game()
        new_game = Game(**base_game)
        new_game.save()
        new_game.genre.add(1)
        new_game.people.add(1)
        request = self.factory.get('api/games/1/people/')
        response = api_games_people(request, 1)
        response_content = response.content.decode('utf-8')
        db_query = serializers.serialize("json", Game.objects.get(pk = 1).people.all(), fields=("name"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content, db_query)

    def test_GET_intersection_games_people_with_bad_id(self):
        request = self.factory.get('api/games/1/people/')
        response = api_games_people(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_intersection_games_companies(self):
        setup_db_for_game()
        new_game = Game(**base_game)
        new_game.save()
        new_game.genre.add(1)
        new_game.people.add(1)
        request = self.factory.get('api/games/1/companies/')
        response = api_games_companies(request, 1)
        response_content = response.content.decode('utf-8')
        db_query = serializers.serialize("json", [Game.objects.get(pk = 1).company], fields=("name"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content, db_query)

    def test_GET_intersection_games_companies_with_bad_id(self):
        request = self.factory.get('api/games/1/companies/')
        response = api_games_people(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

class TestPeople (TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_POST_person(self):
        new_company = Company(**base_company).save()
        request = self.factory.post('api/people/', base_person_input, content_type='application/json')
        response = api_people(request)
        response_content = literal_eval(response.content.decode('utf-8'))
        db_query = literal_eval(serializers.serialize("json",[Person.objects.get(pk = 1)]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content, id_1)
        self.assertDictEqual(db_query[0]["fields"], base_person_post)

    def test_POST_person_with_no_image_key(self):
        new_company = Company(**base_company).save()
        request = self.factory.post('api/people/', base_person_post, content_type='application/json')
        response = api_people(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_person_with_empty_image_key(self):
        new_company = Company(**base_company).save()
        person_data = base_person_input.copy()
        person_data["images"] = []
        request = self.factory.post('api/people/', base_person_post, content_type='application/json')
        response = api_people(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_person_with_no_name(self):
        new_company = Company(**base_company).save()
        person_data = base_person_input.copy()
        person_data.pop("name")
        request = self.factory.post('api/person/', person_data, content_type='application/json')
        response = api_people(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_person_with_empty_name(self):
        new_company = Company(**base_company).save()
        person_data = base_person_input.copy()
        person_data["name"] = " "
        request = self.factory.post('api/person/', person_data, content_type='application/json')
        response = api_people(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_person_with_no_company(self):
        new_company = Company(**base_company).save()
        person_data = base_person_input.copy()
        person_data.pop("companies")
        request = self.factory.post('api/person/', person_data, content_type='application/json')
        response = api_people(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_POST_person_with_empty_company(self):
        new_company = Company(**base_company).save()
        person_data = base_person_input.copy()
        person_data["companies"] = []
        request = self.factory.post('api/person/', person_data, content_type='application/json')
        response = api_people(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_get_all_people(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        request = self.factory.get('api/person/', content_type='application/json')
        response = api_people(request)
        response_content = literal_eval(response.content.decode('utf-8'))
        db_query = literal_eval(serializers.serialize("json", Person.objects.all(), fields=("name")))
        db_query[0]["fields"]["images"] = []
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db_query, response_content)

    def test_PUT_person(self):
        new_company = Company(**base_company).save()
        request = self.factory.post('api/people/', base_person_input, content_type='application/json')
        response = api_people(request)
        request = self.factory.put('api/people/1/', updated_person_input, content_type='application/json')
        response = api_people_id(request, '1')
        response_content = response.content.decode('utf-8')
        person_object = Person.objects.get(pk=1)
        db_query = literal_eval(serializers.serialize("json",[person_object]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(db_query[0]["fields"], updated_person)
        self.assertEqual(person_object.images()[0].link, updated_person_input["images"][0])

    def test_PUT_person_with_bad_id(self):
        request = self.factory.put('api/people/1/', updated_person_input, content_type='application/json')
        response = api_people_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_PUT_person_with_empty_image(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        person_data = base_person_input.copy()
        person_data["images"] = []
        request = self.factory.put('api/people/1/', person_data, content_type='application/json')
        response = api_people_id(request, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_person_with_empty_video(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        person_data = base_person_input.copy()
        person_data["videos"] = []
        request = self.factory.put('api/people/1/', person_data, content_type='application/json')
        response = api_people_id(request, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_PUT_person_with_empty_name(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        request = self.factory.post('api/people/', base_person_input, content_type='application/json')
        response = api_people(request)
        person_data = base_person_input.copy()
        person_data["name"] = " "
        request = self.factory.put('api/people/1/', person_data, content_type='application/json')
        response = api_people_id(request, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'')

    def test_GET_people(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        request = self.factory.get('api/people/1/')
        response = api_people_id(request, '1')
        person_object = Person.objects.get(pk=1)
        db_query = literal_eval(serializers.serialize("json",[person_object]))
        response_content = literal_eval(response.content.decode('utf-8'))
        image_link = response_content[0]["fields"].pop("images")
        video_link = response_content[0]["fields"].pop("videos")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db_query, response_content)
        self.assertEqual(len(image_link), 0)
        self.assertEqual(len(video_link), 0)

    def test_GET_with_bad_id(self):
        request = self.factory.get('api/people/1/')
        response = api_people_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_DELETE_person(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        request = self.factory.delete('api/people/1/')
        response = api_people_id(request, '1')
        self.assertEqual(len(Images.objects.filter(other_id = 1, other_type = 'CP')), 0)
        self.assertEqual(len(Person.objects.filter(pk = 1)), 0)
        self.assertEqual(response.status_code, 204)

    def test_DELETE_with_bad_id(self):
        request = self.factory.delete('api/people/1/')
        response = api_people_id(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_intersection_people_games(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        System(**base_system).save()
        Genre(**base_genre).save()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        api_games(request)
        request = self.factory.get('api/people/1/games/')
        response = api_people_games(request, 1)
        response_content = response.content.decode('utf-8')
        db_query = serializers.serialize("json", Game.objects.filter(people = 1), fields=("name"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content, db_query)

    def test_GET_intersection_people_games_with_bad_id(self):
        request = self.factory.get('api/people/1/games/')
        response = api_people_games(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

    def test_GET_intersection_people_company(self):
        new_company = Company(**base_company).save()
        new_person = Person(**base_person)
        new_person.save()
        new_person.companies.add(1)
        request = self.factory.get('api/people/1/companies/')
        response = api_people_companies(request, 1)
        response_content = response.content.decode('utf-8')
        db_query = serializers.serialize("json", Company.objects.filter(person = 1), fields=("name"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content, db_query)

    def test_GET_intersection_people_companies_with_bad_id(self):
        request = self.factory.get('api/people/1/companies/')
        response = api_people_companies(request, '1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'')

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
        response_content = literal_eval(response.content.decode('utf-8'))
        db_query = literal_eval(serializers.serialize("json", Company.objects.all(), fields=("name")))
        db_query[0]["fields"]["images"] = []
        db_query[1]["fields"]["images"] = []
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
        self.assertEqual(response.status_code, 204)
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

# -----------
# Test Search
# -----------
class TestSearch (TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_search_game(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.get('search/?q=game')
        response = search_query(request, 'game')
        name = response[0]['name']
        rank = response[0]['rank']
        self.assertEqual(name, 'game')
        self.assertEqual(rank, 8)
        
    def test_search_company(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.get('search/?q=Company')
        response = search_query(request, 'Company')
        name = response[0]['name']
        rank = response[0]['rank']
        self.assertEqual(name, 'Company')
        self.assertEqual(rank, 6)

    def test_search_people(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.get('search/?q=person')
        response = search_query(request, 'person')
        name = response[0]['name']
        rank = response[0]['rank']
        self.assertEqual(name, 'person')
        self.assertEqual(rank, 5)

    def test_search_empty(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.get('search/?q=')
        response = search_query(request, '')
        self.assertEqual(response, [])

    def test_search_not_found(self):
        setup_db_for_game()
        request = self.factory.post('api/games/', base_game_input, content_type='application/json')
        response = api_games(request)
        request = self.factory.get('search/?q=silly')
        response = search_query(request, '')
        self.assertEqual(response, [])
print("tests.py")
print("Done.")