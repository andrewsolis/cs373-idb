#!/usr/bin/env python3

import unittest
from json import dumps
from urllib.request import Request, urlopen
from ast import literal_eval

machine_name = "oh-henry"
port = "5009"
endpoint = "http://" + machine_name + ":" + port + "/api/"

game_example = [{"pk": 1, "model": "videogames.game", "fields": {"name": "Metroid", "images": ["http://upload.wikimedia.org/wikipedia/en/5/5d/Metroid_boxart.jpg"], "people": [1], "release_date": "1986-08-06T00:00:00Z", "system": "NES", "copies": 273000, "gamefaq": "http://www.gamefaqs.com/nes/519689-metroid", "synopsis": "description for metroid", "videos": ["www.youtube.com/embed/WT4pW6n7-rg"], "genre": ["Side Scroller"], "company": 1}}]
full_game_list = [{"pk": 1, "model": "videogames.game", "fields": {"name": "Metroid"}}, {"pk": 2, "model": "videogames.game", "fields": {"name": "Sonic the Hedgehog"}}, {"pk": 3, "model": "videogames.game", "fields": {"name": "Crash Bandicoot"}}, {"pk": 4, "model": "videogames.game", "fields": {"name": "Super Mario Bros. 3"}}, {"pk": 5, "model": "videogames.game", "fields": {"name": "Bomberman"}}, {"pk": 6, "model": "videogames.game", "fields": {"name": "Super Street Fighter II"}}, {"pk": 7, "model": "videogames.game", "fields": {"name": "The Legend of Zelda: A Link to the Past"}}, {"pk": 8, "model": "videogames.game", "fields": {"name": "Donkey Kong Country"}}, {"pk": 9, "model": "videogames.game", "fields": {"name": "Mortal Kombat II"}}]

people_example = [{"pk": 1, "model": "videogames.person", "fields": {"name": "Yoshio Sakamoto", "videos": ["https://www.youtube.com/watch?v=eBuWOKsK2JE"], "DOB": "1959-07-23T00:00:00Z", "residence": "Kyoto, Japan", "twitter": "", "companies": [1], "images": ["http://upload.wikimedia.org/wikipedia/commons/3/3d/Yoshio_Sakamoto_-_Game_companys_Conference_2010_-_Day_3_%282%29_cropped.jpg"], "description": "description for Yoshio"}}]
full_people_list = [{"pk": 1, "model": "videogames.person", "fields": {"name": "Yoshio Sakamoto"}}, {"pk": 2, "model": "videogames.person", "fields": {"name": "Naoto Oshima"}}, {"pk": 3, "model": "videogames.person", "fields": {"name": "Andy Gavin"}}, {"pk": 4, "model": "videogames.person", "fields": {"name": "Shigeru Miyamoto"}}, {"pk": 5, "model": "videogames.person", "fields": {"name": "Takahashi"}}, {"pk": 6, "model": "videogames.person", "fields": {"name": "Kenzo Tsujimoto"}}, {"pk": 7, "model": "videogames.person", "fields": {"name": "Daniel Owsen"}}, {"pk": 8, "model": "videogames.person", "fields": {"name": "Ed Boon"}}]

company_example = [{"pk": 1, "model": "videogames.company", "fields": {"mapimage": "http://goo.gl/maps/1KSBf", "description": "description for nintendo", "webpage": "http://www.nintendo.com/", "founded": "1889-01-01T00:00:00Z", "location": "Kyoto, Japan", "images": ["http://ugrgaming.com/wp-content/uploads/2013/01/Nintendo-Logo.jpg"], "name": "Nintendo"}}]
full_company_list = [{"pk": 1, "model": "videogames.company", "fields": {"name": "Nintendo"}}, {"pk": 2, "model": "videogames.company", "fields": {"name": "Sega"}}, {"pk": 3, "model": "videogames.company", "fields": {"name": "Naughty Dog"}}, {"pk": 4, "model": "videogames.company", "fields": {"name": "Hudson Soft"}}, {"pk": 5, "model": "videogames.company", "fields": {"name": "Capcom"}}, {"pk": 6, "model": "videogames.company", "fields": {"name": "Rare"}}, {"pk": 7, "model": "videogames.company", "fields": {"name": "Midway"}}, {"pk": 8, "model": "videogames.company", "fields": {"name": "Electronic Arts"}}, {"pk": 9, "model": "videogames.company", "fields": {"name": "Square"}}, {"pk": 10, "model": "videogames.company", "fields": {"name": "Westwood Studios"}}]
company_added = {"mapimage": "http://goo.gl/maps/1KSBf", "description": "description for nintendo", "webpage": "http://www.nintendo.com/", "founded": "1889-01-01T00:00:00Z", "location": "Kyoto, Japan", "images": ["http://work.com"], "name": "Mitchendo"}
full_company_added = [{"pk": 11, "model": "videogames.company", "fields": {"mapimage": "http://goo.gl/maps/1KSBf", "description": "description for nintendo", "webpage": "http://www.nintendo.com/", "founded": "1889-01-01T00:00:00Z", "location": "Kyoto, Japan", "images": ["http://work.com"], "name": "Mitchendo"}}]

no_content = b''

# --------
# Test API
# --------

class TestGames (unittest.TestCase):
    
    def test_list_all_games(self):
        
        request = Request(endpoint + "games")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == full_game_list)
        self.assertTrue(response.getcode() == 200)
        


#     def test_add_game(self):
#         values = dumps(game_example).encode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         request = Request(endpoint + "games", data=values, headers=headers)
#         response = urlopen(request)
#         response_body = literal_eval(response.read().decode('utf-8'))
#         self.assertTrue(response_body == id_dic)
#         self.assertTrue(response.getcode() == 201)

    def test_game_info(self):
        request = Request(endpoint + "games/1/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body[0]["pk"] == 1)
        self.assertTrue(response_body == game_example)
        self.assertTrue(response.getcode() == 200)

#   def test_update_game(self):
#       values = dumps(game_example).encode('utf-8')
#       headers = {"Content-Type": "application/json"}
#       request = Request(endpoint + "games/1/", data=values, headers=headers)
#       request.get_method = lambda: 'PUT'
#       response = urlopen(request)
#       response_body = response.read()
#       # print(response_body)
#       self.assertTrue(response_body == no_content)
#       self.assertTrue(response.getcode() == 204)

#     def test_delete_game(self):
#         request = Request(endpoint + "games/{id}")
#         request.get_method = lambda: 'DELETE'
#         response = urlopen(request)
#         response_body = response.read()
#         self.assertTrue(response_body == no_content)
#         self.assertTrue(response.getcode() == 204)

    def test_list_companies_by_game(self):
        request = Request(endpoint + "games/1/companies/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == [{"pk": 1, "model": "videogames.company", "fields": {"name": "Nintendo"}}])
        self.assertTrue(response.getcode() == 200)
        
    def test_list_people_by_game(self):
        request = Request(endpoint + "games/1/people/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == [{"pk": 1, "model": "videogames.person", "fields": {"name": "Yoshio Sakamoto"}}])
        self.assertTrue(response.getcode() == 200)

class TestPeople(unittest.TestCase):

    def test_list_all_people(self):
        request = Request(endpoint + "people")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == full_people_list)
        self.assertTrue(response.getcode() == 200)

#     def test_add_person(self):
#         values = dumps(people_example).encode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         request = Request(endpoint + "people", data=values, headers=headers)
#         response = urlopen(request)
#         response_body = literal_eval(response.read().decode('utf-8'))
#         self.assertTrue(response_body == id_dic)
#         self.assertTrue(response.getcode() == 201)

    def test_people_info(self):
        request = Request(endpoint + "people/1/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body[0]["pk"] == 1)
        self.assertTrue(response_body == people_example)
        self.assertTrue(response.getcode() == 200)

#     def test_update_people(self):
#         values = dumps(people_example).encode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         request = Request(endpoint + "people/{id}", data=values, headers=headers)
#         request.get_method = lambda: 'PUT'
#         response = urlopen(request)
#         response_body = response.read()
#         self.assertTrue(response_body == no_content)
#         self.assertTrue(response.getcode() == 204)

#     def test_delete_people(self):
#         request = Request(endpoint + "people/{id}")
#         request.get_method = lambda: 'DELETE'
#         response = urlopen(request)
#         response_body = response.read()
#         self.assertTrue(response_body == no_content)
#         self.assertTrue(response.getcode() == 204)

    def test_list_games_by_people(self):
        request = Request(endpoint + "people/1/games/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == [{"pk": 1, "model": "videogames.game", "fields": {"name": "Metroid"}}])
        self.assertTrue(response.getcode() == 200)

    def test_list_companies_by_people(self):
        request = Request(endpoint + "people/1/companies/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == [{"pk": 1, "model": "videogames.company", "fields": {"name": "Nintendo"}}])
        self.assertTrue(response.getcode() == 200)

class TestCompanies(unittest.TestCase):

    def test_list_all_companies(self):
        request = Request(endpoint + "companies")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == full_company_list)
        self.assertTrue(response.getcode() == 200)

    # def test_add_company(self):
    #     values = dumps(company_added).encode('utf-8')
    #     headers = {"Content-Type": "application/json"}
    #     request = Request(endpoint + "companies", data=values, headers=headers)
    #     response = urlopen(request)
    #     response_body = literal_eval(response.read().decode('utf-8'))
    #     self.assertTrue(response.getcode() == 201)
    #     added_id = int(response_body["id"])
    #     full_company_added[0]["pk"] == added_id

    #     request = Request(endpoint + "companies/" + str(id_added) + "/")
    #     response = urlopen(request)
    #     response_body = literal_eval(response.read().decode('utf-8'))
    #     self.assertTrue(response_body[0]["pk"] == added_id)
    #     self.assertTrue(response_body == company_example)
    #     self.assertTrue(response.getcode() == 200)

    def test_company_info(self):
        request = Request(endpoint + "companies/1/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body[0]["pk"] == 1)
        self.assertTrue(response_body == company_example)
        self.assertTrue(response.getcode() == 200)

#     def test_update_company(self):
#         values = dumps(company_example).encode('utf-8')
#         headers = {"Content-Type": "application/json"}
#         request = Request(endpoint + "companies/{id}", data=values, headers=headers)
#         request.get_method = lambda: 'PUT'
#         response = urlopen(request)
#         response_body = response.read()
#         self.assertTrue(response_body == no_content)
#         self.assertTrue(response.getcode() == 204)

#     def test_delete_company(self):
#         request = Request(endpoint + "companies/{id}")
#         request.get_method = lambda: 'DELETE'
#         response = urlopen(request)
#         response_body = response.read()
#         self.assertTrue(response_body == no_content)
#         self.assertTrue(response.getcode() == 204)

    def test_list_games_by_company(self):
        request = Request(endpoint + "companies/1/games/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == [{"pk": 1, "model": "videogames.game", "fields": {"name": "Metroid"}}, {"pk": 4, "model": "videogames.game", "fields": {"name": "Super Mario Bros. 3"}}, {"pk": 7, "model": "videogames.game", "fields": {"name": "The Legend of Zelda: A Link to the Past"}}])
        self.assertTrue(response.getcode() == 200)

    def test_list_people_by_company(self):
        request = Request(endpoint + "companies/1/people/")
        response = urlopen(request)
        response_body = literal_eval(response.read().decode('utf-8'))
        self.assertTrue(response_body == [{"pk": 1, "model": "videogames.person", "fields": {"name": "Yoshio Sakamoto"}}, {"pk": 4, "model": "videogames.person", "fields": {"name": "Shigeru Miyamoto"}}])
        self.assertTrue(response.getcode() == 200)

print("tests.py")
unittest.main()
print("Done.")