#!/usr/bin/python
from catalog import DefeCatalog
from dbconnector import DBConnector

import json


class GranDT(object):
	def  __init__(self, catalog):
		self.catalog = catalog
		self.conn = DBConnector(catalog.db_name)

	def check_valid_user(self,email):
		query = self.catalog.query_to_check_valid_user(email)
		_cursor = self.conn.execute_query(query)
		return _cursor.fetchone()

	def get_player_id(self, player):
		''' Each player inside is a tuple of name and category '''
		p_name, p_category = player
		query = self.catalog.query_get_player_id_by_name_and_category(p_name, p_category)
		_cursor = self.conn.execute_query(query)
		value = _cursor.fetchone()
		if value:
			res = value[0]
		else:
			raise Exception("Player {} from category {} isn't valid player.".format(p_name, p_category))
		return res


	def add_player(self, name, position, category):
		query = self.catalog.query_to_add_player(name, position, category)
		self.conn.execute_query(query)

	def add_user(self, email, user_name, team_name, players):
		players_ids = [self.get_player_id(player) for player in players]
		categories = [category for _, category in players]		
		query = self.catalog.query_to_add_user_and_team(email, user_name, team_name, players_ids, categories)
		self.conn.execute_query(query)

	def change_team(self, email, players):
		valid_user = self.check_valid_user(email)
		if valid_user:
			players_ids = [self.get_player_id(player) for player in players]
			categories = [category for _, category in players]	
			query = self.catalog.query_to_change_team(email, players_ids, categories)
			self.conn.execute_query(query)
		else:
			raise Exception("User with email: {} doesn't exists.".format(email))



	def add_round(self,_round):
		''' FORMAT OF JSON
		{
			number: n,
			stats: {
				category:{
					p_name':{
						'goals': x,
						'yellow': y,		
					}
				}
			}
		}
		'''

		_round = json.loads(_round)
		round_num = _round['number']
		stats = 'stats'
		for category in _round[stats].keys():
			for player_name in _round[stats][category].keys():
				player_id = self.get_player_id((player_name, category))	
				stats_of_player = _round[stats][category][player_name]
				query = self.catalog.query_to_add_player_statistics_of_round(round_num, player_id, stats_of_player)
				print query
				return
				self.conn.execute_query(query)


	

if __name__ == '__main__':
	catalog = DefeCatalog()
	gdt = GranDT(catalog)

	#gdt.add_player('Gonza', 'delanteRo', 'SuperIOR')
	#gdt.add_player('Partu', 'delanteRo', 'Juveniles')
	#gdt.add_player('Mudo', 'delanteRo', 'menores')
	#gdt.add_player('Mono', 'delanteRo', 'menores')
	#gdt.add_player('Tebi', 'delanteRo', 'Cadetes')
	#gdt.add_user('a@a.com', 'loco', 'locos', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])

	# gdt.change_team('b@a.com', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])
	


	a = {"number": 1, "stats": {"Superior": {"Gonza": {"present": 1,"absent": 1,"mvp": 1,"pen_goals": 1,"goals": 1,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 1,"blue_card": 1,"miss_pen": 1,"saved_pen": 1}}}}
	a = json.dumps(a)
	gdt.add_round(a)