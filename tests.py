#!/usr/bin/env python2.7

import io
import unittest
import sys
from json import dumps, loads
from urllib2 import Request, urlopen
from ast import literal_eval

# --------
# Test API
# --------

endpoint = "http://idb1.apiary.io/api/"

game_full = { "name": "Metroid", "system": "NES", "release_date": "1986-08-06", "genre": ["action-adventure", "side-scroller"], "synopsis": "Long text describing Metroid", "copies_sold": 2730000, "images": ["http://upload.wikimedia.org/wikipedia/en/5/5d/Metroid_boxart.jpg"], "gameFAQ" : "http://www.gamefaqs.com/nes/519689-metroid", "videos": ["https://www.youtube.com/watch?v=WT4pW6n7-rg"], "people": [1], "companies": [1], }
game_short = [{ "name": "Metroid", "id": 1, "system": "NES", }]

people_full = { "name": "Yoshio Sakamoto", "DOB": "1959-07-23", "location": "Kyoto, Japan", "job": {1: "Director"}, "description": "Long text description for Yoshio", "images": ["http://upload.wikimedia.org/wikipedia/commons/3/3d/Yoshio_Sakamoto_-_Game_Developers_Conference_2010_-_Day_3_%282%29_cropped.jpg"], "videos": ["https://www.youtube.com/watch?v=eBuWOKsK2JE"], "games": [1], "companies": [1], }

company_full = { "name": "Nintendo", "founded": "1889", "location": "Kyoto, Japan", "description": "Long text description for Nintendo", "images": ["http://ugrgaming.com/wp-content/uploads/2013/01/Nintendo-Logo.jpg"], "map": ["http://goo.gl/maps/1KSBf"], "external_links": ["http://www.nintendo.com/"], "people": [1], "games": [1], }
company_short = [{ "name": "Nintendo", "id": 1, }]

id_dic = { "id": 1 }


class TestGames (unittest.TestCase):
    
    def test_list_all_games(self):
        request = Request(endpoint + "games")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == game_short)
        self.assertTrue(response.getcode() == 200)

    def test_add_game(self):
        values = dumps(game_full)
        headers = {"Content-Type": "application/json"}
        request = Request(endpoint + "games", data=values, headers=headers)
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == id_dic)
        self.assertTrue(response.getcode() == 201)

    def test_game_info(self):
        request = Request(endpoint + "games/{id}")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body.get("id") == 1)
        response_body.pop("id", 1)
        self.assertTrue(response_body == game_full)
        self.assertTrue(response.getcode() == 200)

    def test_update_game(self):
        values = dumps(game_full)
        headers = {"Content-Type": "application/json"}
        request = Request(endpoint + "games/{id}", data=values, headers=headers)
        request.get_method = lambda: 'PUT'
        response = urlopen(request)
        response_body = response.read()
        self.assertTrue(response_body == '')
        self.assertTrue(response.getcode() == 204)

    def test_delete_game(self):
        request = Request(endpoint + "games/{id}")
        request.get_method = lambda: 'DELETE'
        response = urlopen(request)
        response_body = response.read()
        self.assertTrue(response_body == '')
        self.assertTrue(response.getcode() == 204)

    def test_list_companies_by_game(self):
        request = Request(endpoint + "games/{id}/companies")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == company_short)
        self.assertTrue(response.getcode() == 200)
        
    def test_list_people_by_game(self):
        request = Request(endpoint + "games/{id}/people")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == [{"name": "Yoshio Sakamoto", "id": 1, "job": "Director", }])
        self.assertTrue(response.getcode() == 200)

class TestPeople(unittest.TestCase):

    def test_list_all_people(self):
        request = Request(endpoint + "people")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == [{"name": "Yoshio Sakamoto", "id": 1, "job": {1: "Director"}, }])
        self.assertTrue(response.getcode() == 200)

    def test_add_person(self):
        values = dumps(people_full)
        headers = {"Content-Type": "application/json"}
        request = Request(endpoint + "people", data=values, headers=headers)
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == id_dic)
        self.assertTrue(response.getcode() == 201)

    def test_people_info(self):
        request = Request(endpoint + "people/{id}")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body.get("id") == 1)
        response_body.pop("id", 1)
        self.assertTrue(response_body == people_full)
        self.assertTrue(response.getcode() == 200)

    def test_update_people(self):
        values = dumps(people_full)
        headers = {"Content-Type": "application/json"}
        request = Request(endpoint + "people/{id}", data=values, headers=headers)
        request.get_method = lambda: 'PUT'
        response = urlopen(request)
        response_body = response.read()
        self.assertTrue(response_body == '')
        self.assertTrue(response.getcode() == 204)

    def test_delete_people(self):
        request = Request(endpoint + "people/{id}")
        request.get_method = lambda: 'DELETE'
        response = urlopen(request)
        response_body = response.read()
        self.assertTrue(response_body == '')
        self.assertTrue(response.getcode() == 204)

    def test_list_games_by_people(self):
        request = Request(endpoint + "people/{id}/games")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == game_short)
        self.assertTrue(response.getcode() == 200)

    def test_list_companies_by_people(self):
        request = Request(endpoint + "people/{id}/companies")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == company_short)
        self.assertTrue(response.getcode() == 200)

class TestCompanies(unittest.TestCase):

    def test_list_all_companies(self):
        request = Request(endpoint + "companies")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == company_short)
        self.assertTrue(response.getcode() == 200)

    def test_add_company(self):
        values = dumps(company_full)
        headers = {"Content-Type": "application/json"}
        request = Request(endpoint + "companies", data=values, headers=headers)
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == id_dic)
        self.assertTrue(response.getcode() == 201)

    def test_company_info(self):
        request = Request(endpoint + "companies/{id}")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body.get("id") == 1)
        response_body.pop("id", 1)
        self.assertTrue(response_body == company_full)
        self.assertTrue(response.getcode() == 200)

    def test_update_company(self):
        values = dumps(company_full)
        headers = {"Content-Type": "application/json"}
        request = Request(endpoint + "companies/{id}", data=values, headers=headers)
        request.get_method = lambda: 'PUT'
        response = urlopen(request)
        response_body = response.read()
        self.assertTrue(response_body == '')
        self.assertTrue(response.getcode() == 204)

    def test_delete_company(self):
        request = Request(endpoint + "companies/{id}")
        request.get_method = lambda: 'DELETE'
        response = urlopen(request)
        response_body = response.read()
        self.assertTrue(response_body == '')
        self.assertTrue(response.getcode() == 204)

    def test_list_games_by_company(self):
        request = Request(endpoint + "companies/{id}/games")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == game_short)
        self.assertTrue(response.getcode() == 200)

    def test_list_people_by_company(self):
        request = Request(endpoint + "companies/{id}/people")
        response = urlopen(request)
        response_body = literal_eval(response.read())
        self.assertTrue(response_body == [{"name": "Yoshio Sakamoto", "id": 1, }])
        self.assertTrue(response.getcode() == 200)

print("tests.py")
unittest.main()
print("Done.")