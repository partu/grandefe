#!/usr/bin/python 
import constants

from gran_dt import GranDT 
from catalog import DefeCatalog
from dbconnector import DBConnector


class Tester(object):
	def __init__(self, db_name):
		self.catalog = DefeCatalog(db_name)
		self.gdt = GranDT(self.catalog)


class test_add_player_invalid_category(Tester):
	def __init__(self):
		super(test_add_player_invalid_category, self).__init__(self.__class__)

		player_name = 'gonza' 
		category = 'Superior'
		position = "Delantero"


test_add_team_no_more_than_5_players
test_add_team_no_less_than_5_players
test_add_team_no_repeated_players
test_add_team_all_valid_players

def test_update_with_invalid_user():
	gdt.add_player('Gonza', 'delanteRo', 'SuperIOR')
	gdt.add_player('Partu', 'delanteRo', 'Juveniles')
	gdt.add_player('Mudo', 'delanteRo', 'menores')
	gdt.add_player('Mono', 'delanteRo', 'menores')
	gdt.add_player('Tebi', 'delanteRo', 'Cadetes')
	#gdt.add_user('a@a.com', 'loco', 'locos', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])
	gdt.change_team('b@a.com', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])




