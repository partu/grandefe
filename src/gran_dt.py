#!/usr/bin/python
import collections
import constants
import json

from catalog import DefeCatalog
from dbconnector import DBConnector

from constants import ROUND_NUMBER, STATS, NAME, CATEGORY, POSITION, VALUES

Player = collections.namedtuple('Player',['name', 'position', 'category'])
Team = collections.namedtuple('Team',['key', 'titulars', 'alternates'])


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


	def get_players_that_will_count(self, team, _round):
		players = []
		#Check that the 5 titulars played
		query = self.catalog.query_get_present_players(_round, team.titulars)
		present_titulars = [value[0] for value in self.conn.execute_query(query).fetchall()]

		print "Titulars: ", team.titulars
		print "Prenset titulars: ", present_titulars

		#If all titulars played
		if len(present_titulars) == constants.NUMBER_OF_TITULARS:
			return present_titulars

		else:
			#use the alternate player for the missing titulars
			absent_titulars = filter(lambda _id: _id not in present_titulars, team.titulars)
			print 'absent_titulars: ' , absent_titulars
			query = self.catalog.query_get_positions_of_players(absent_titulars)
			print query
			missing_positions = self.conn.execute_query(query).fetchall()
			print "Miss pos: " , missing_positions


			#####HAY QUE TRAER LOS SUPLLENTES DE ESTE EQUIPO QUE TIENEN LA MISMA POSICION DE MISSING Y QUE JUGARON ESA VEZ! 












	def add_player(self, player):
		query = self.catalog.query_to_add_player(player)
		self.conn.execute_query(query)


	def add_user(self, dni, user_name, team_name, players):
		players_info = [(self.get_player_id(player), player , tit) for player, tit in players]
		query = self.catalog.query_to_add_user_and_team(dni, user_name, team_name, players_info)
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


	def add_round(self,_round):
		''' FORMAT OF JSON
	{
		round_number: n,
		stats:[
				{ 
				name: ,
				cat: ,
				pos: ,
				values: {
					"present": 1,
					"absent": 1,
					"mvp": 1,
					"pen_goals": 1,
					"goals": 1,
					"against_goals": 1,
					"own_goals": 1,
					"yellow_card": 1,
					"red_card": 1,
					"blue_card": 1,
					"miss_pen": 1,
					"saved_pen": 1,
				},

		}
	}
	# 	'''

		info = json.loads(_round)
		round_num = info[ROUND_NUMBER]
		stats = info[STATS]
		#Add players values to history
		for p_stats in stats:
			
			player = Player(p_stats[NAME],p_stats[POSITION],p_stats[CATEGORY])
			player_id = self.get_player_id(player)
			player_values = p_stats[VALUES]
		
			#Calculate total points of this player	
			query = self.catalog.query_all_actions_points_for_position(player.position)
			_cursor = self.conn.execute_query(query)
			points_per_action = _cursor.fetchall()

			total_points = 0
			for action, points in points_per_action:
				total_points += player_values[action] * points


			#Set the history entry for this player
			query = self.catalog.query_to_set_history_entry(round_num, player_id, total_points, player_values)
			print query
			self.conn.execute_query(query)

		#Once finished updating points of this round for all the players, we continue with the teams! 
		#Update teams points points_of_teams_by_round
		#take into account titularities!!!!

		query = self.catalog.query_get_all_teams()		
		teams = self.conn.execute_query(query).fetchall()
		print teams

		for team in teams:
			#Get players 
			team = Team(team[0], team[1:6], team[6:])
			players_ids = self.get_players_that_will_count(team, round_num)
			calculate_team_points(players_ids)

			return

	

if __name__ == '__main__':
	catalog = DefeCatalog()
	gdt = GranDT(catalog)

	gonza = Player('Gonza', 'delanteRo', 'SuperIOR')
	partu = Player('Partu', 'delanteRo', 'Juveniles')
	mudo = Player('Mudo', 'delanteRo', 'menores')
	mono = Player('Mono', 'DEFENSOR', 'menores')
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


	gdt.add_user(3617541239468, 'loco', 'locos', [(gonza,1),(partu,0),(mudo,1),(mono,0),(tebi,1),(nacho,1),(negro,1),(chola,0),(seba,0)])


#	gdt.change_team('b@a.com', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])
	
	#a = '{"round_number": 1212,"stats":[{ "name": "partu" ,"cat":"JuveNiLes" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}]}'
	a = '{"round_number": 1213,"stats":[{ "name": "partu" ,"cat":"JuveNiLes" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "mudo" ,"cat":"menores" ,"pos": "delantero" ,"values": {"present": 0,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "gonza" ,"cat":"superior" ,"pos": "delantero" ,"values": {"present": 0,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "mono" ,"cat":"menores" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "tebi" ,"cat":"cadetes" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "nacho" ,"cat":"menores" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "negro" ,"cat":"cadetes" ,"pos": "defensor" ,"values": {"present": 0,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "chola" ,"cat":"JuveNiLes" ,"pos": "mediocampista" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}},{ "name": "seba" ,"cat":"superior" ,"pos": "arquero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}]}'

	# a = {"number": 1, "stats": {"Superior": {"Gonza": {"present": 1,"absent": 1,"mvp": 1,"pen_goals": 1,"goals": 1,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 1,"blue_card": 1,"miss_pen": 1,"saved_pen": 1}}}}
	# a = json.dumps(a)
	gdt.add_round(a)