#!/usr/bin/python
import collections
import json

from catalog import DefeCatalog
from dbconnector import DBConnector


Player = collections.namedtuple('Player',['name', 'position', 'category'])



class GranDT(object):
	def  __init__(self, catalog):
		self.catalog = catalog
		self.conn = DBConnector(catalog.db_name)

	def check_valid_user(self,dni):
		query = self.catalog.query_to_check_valid_user(dni)
		_cursor = self.conn.execute_query(query)
		return _cursor.fetchone()

	def get_player_id(self, player):
		query = self.catalog.query_get_player_id_by_name_and_category(player)
		_cursor = self.conn.execute_query(query)
		value = _cursor.fetchone()
		if value:
			res = value[0]
		else:
			raise Exception("Player {} from category {} isn't valid player.".format(player.name, player.category))
		return res


	def add_player(self, player):
		query = self.catalog.query_to_add_player(player)
		self.conn.execute_query(query)


	def add_user(self, dni, user_name, team_name, players):
		players_info = [(self.get_player_id(player), player , tit) for player, tit in players]
		query = self.catalog.query_to_add_user_and_team(dni, user_name, team_name, players_info)
		print query
		self.conn.execute_query(query)

	def change_team(self, dni, players):
		raise Exception("We aren't using it up to now")
		valid_user = self.check_valid_user(dni)
		if valid_user:
			players_ids = [self.get_player_id(player) for player in players]
			categories = [category for _, category in players]	
			query = self.catalog.query_to_change_team(dni, players_ids, categories)
			self.conn.execute_query(query)
		else:
			raise Exception("User with dni: {} doesn't exists.".format(dni))



	# def add_round(self,_round):
	# 	''' FORMAT OF JSON
	# 	{
	# 		number: n,
	# 		stats: {
	# 			category:{
	# 				p_name':{
	# 					'goals': x,
	# 					'yellow': y,		
	# 				}
	# 			}
	# 		}
	# 	}
	# 	'''

	# 	_round = json.loads(_round)
	# 	round_num = _round['number']
	# 	stats = 'stats'
	# 	for category in _round[stats].keys():
	# 		for player_name in _round[stats][category].keys():
	# 			player_id = self.get_player_id((player_name, category))	
	# 			stats_of_player = _round[stats][category][player_name]
	# 			query = self.catalog.query_to_add_player_statistics_of_round(round_num, player_id, stats_of_player)
	# 			print query
	# 			return
	# 			self.conn.execute_query(query)


	

if __name__ == '__main__':
	catalog = DefeCatalog()
	gdt = GranDT(catalog)

	gonza = Player('Gonza', 'delanteRo', 'SuperIOR')
	partu = Player('Partu', 'delanteRo', 'Juveniles')
	mudo = Player('Mudo', 'delanteRo', 'menores')
	mono = Player('Mono', 'delanteRo', 'menores')
	tebi = Player('Tebi', 'delanteRo', 'Cadetes')
	nacho = Player('Nacho', 'delanteRo', 'Menores')
	negro = Player('Negro', 'defensor', 'Cadetes')
	chola = Player('Chola', 'mediocampista', 'Juveniles')
	seba = Player('Seba', 'arquero', 'Superior')


	gdt.add_player(gonza)
	gdt.add_player(partu)
	gdt.add_player(mudo)
	gdt.add_player(mono)
	gdt.add_player(tebi)
	gdt.add_player(nacho)
	gdt.add_player(negro)
	gdt.add_player(chola)
	gdt.add_player(seba)


	gdt.add_user(36754945, 'loco', 'locos', [(gonza,1),(partu,1),(mudo,1),(mono,0),(tebi,1),(nacho,1),(negro,0),(chola,0),(seba,0)])


#	gdt.change_team('b@a.com', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])
	

	# a = {"number": 1, "stats": {"Superior": {"Gonza": {"present": 1,"absent": 1,"mvp": 1,"pen_goals": 1,"goals": 1,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 1,"blue_card": 1,"miss_pen": 1,"saved_pen": 1}}}}
	# a = json.dumps(a)
	# gdt.add_round(a)