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


def test_one_alternate_per_postion():
	catalog = DefeCatalog()
	gdt = GranDT(catalog)

	gonza = Player('Gonza', 'delanteRo', 'SuperIOR')
	partu = Player('Partu', 'delanteRo', 'Juveniles')
	mudo = Player('Mudo', 'delanteRo', 'menores')
	mono = Player('Mono', 'delanteRo', 'menores')
	tebi = Player('Tebi', 'delanteRo', 'Cadetes')
	nacho = Player('Nacho', 'delanteRo', 'Cadetes')
	negro = Player('Negro', 'delanteRo', 'Cadetes')
	chola = Player('Chola', 'delanteRo', 'Cadetes')
	seba = Player('Seba', 'delanteRo', 'Cadetes')


	gdt.add_player(gonza)
	gdt.add_player(partu)
	gdt.add_player(mudo)
	gdt.add_player(mono)
	gdt.add_player(tebi)
	gdt.add_player(nacho)
	gdt.add_player(negro)
	gdt.add_player(chola)
	gdt.add_player(seba)


	gdt.add_user('a@a.com', 'loco', 'locos', [(gonza,1),(partu,1),(mudo,1),(mono,1),(tebi,1),(nacho,0),(negro,0),(chola,0),(seba,0)])


def test_update_with_invalid_user():
	gdt.add_player('Gonza', 'delanteRo', 'SuperIOR')
	gdt.add_player('Partu', 'delanteRo', 'Juveniles')
	gdt.add_player('Mudo', 'delanteRo', 'menores')
	gdt.add_player('Mono', 'delanteRo', 'menores')
	gdt.add_player('Tebi', 'delanteRo', 'Cadetes')
	#gdt.add_user('a@a.com', 'loco', 'locos', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])
	gdt.change_team('b@a.com', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])

def test_minor_than_9_players():
	catalog = DefeCatalog()
	gdt = GranDT(catalog)

	gonza = Player('Gonza', 'delanteRo', 'SuperIOR')
	partu = Player('Partu', 'delanteRo', 'Juveniles')
	mudo = Player('Mudo', 'delanteRo', 'menores')
	mono = Player('Mono', 'delanteRo', 'menores')
	tebi = Player('Tebi', 'delanteRo', 'Cadetes')



	gdt.add_player(gonza)
	gdt.add_player(partu)
	gdt.add_player(mudo)
	gdt.add_player(mono)
	gdt.add_player(tebi)


	gdt.add_user('a@a.com', 'loco', 'locos', [(gonza,1),(partu,1),(mudo,1),(mono,1),(tebi,1)])


