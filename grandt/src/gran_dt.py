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


	def init_db(self):
		self.conn.init_db_with_catalog(catalog)


	def check_valid_user(self,dni):
		query = self.catalog.query_to_check_valid_user(dni)
		_cursor = self.conn.execute_query(query)
		return _cursor.fetchone()

	def get_player_id(self, player):
		query = self.catalog.query_get_player_id_by_name_category_and_position(player)
		_cursor = self.conn.execute_query(query)
		value = _cursor.fetchone()
		if value:
			res = value[0]
		else:
			raise Exception("Player {} from category {} isn't valid player.".format(player.name, player.category))
		return res


	def calculate_team_points(self, round_num, players_ids):
		''' Take into account that if a tuple is present inside the players ids is because you have the option to choose 
		between that two players. The decision must be the one that has more points '''
		#Do we have to choose ? 
		choose = None
		flatten_ids = []
		# print "Ids before flattening: ", players_ids
		
		for elem in players_ids:
			if isinstance(elem, tuple):
				choose = elem
				flatten_ids.extend(list(elem))
			else:
				flatten_ids.append(elem)
		# print "Ids after flattening: ", flatten_ids

		query = self.catalog.get_points_for_player_id_in_round(round_num, flatten_ids)
		player_id_points = self.conn.execute_query(query).fetchall()

		# print "Points per player before choosing: ", player_id_points
		if choose:
			candidates = filter(lambda x: x[0] in choose, player_id_points)
			looser = min(candidates, key= lambda x: x[1])
			index_of_looser = player_id_points.index(looser)
			player_id_points.pop(index_of_looser)


		# print "Points per player after choosing: ", player_id_points
		# print "TOtal points of team : ", sum(points for _, points in player_id_points)
		return sum(points for _, points in player_id_points)


	def get_players_that_will_count(self, team, _round):
		all_team_players = team.titulars  + team.alternates

		#Check which players played
		query = self.catalog.query_get_if_present_players_and_positions(_round, all_team_players)
		players_info = self.conn.execute_query(query).fetchall()
		present_alternates_info = [(_id, pos, prst) for _id, pos, prst in players_info if _id in team.alternates and prst == 1 ]

		present_titulars_ids = [_id for _id, _, present in players_info if _id in team.titulars and present == 1]

		# print "Present titulars :", present_titulars_ids
		# print "Present alternates: ", [_id for _id,_,_ in present_alternates_info]
		#If all titulars played
		if len(present_titulars_ids) == constants.NUMBER_OF_TITULARS:
			return present_titulars_ids

		else:
			playing_players = present_titulars_ids
			#use the alternate player for the missing titulars
			absent_titulars_ids = list(filter(lambda _id: _id not in present_titulars_ids, team.titulars))
			missing_positions = [pos for _id, pos, _  in players_info if _id in absent_titulars_ids]
			# print "absent titulars: ", absent_titulars_ids
			# print "Miss pos: " , missing_positions

			counter = collections.Counter()
			for pos in missing_positions:
				counter[pos] += 1



			#print 'PLaying players before change', playing_players
			#Use the alternate players of each missing position
			for pos, count in counter.most_common():
				possible_players = filter(lambda x: x[1] == pos, present_alternates_info)
				if possible_players:
					res = []
					for player in possible_players:
						index_of_new_player = present_alternates_info.index(player) 
						new_player_id, _ , _ = present_alternates_info.pop(index_of_new_player)
						res.append(new_player_id)
					
					if count == 1:
						res = tuple(res) if len(res) == 2 else res[0]
						playing_players.append(res)
					
					elif count == 2:
						playing_players.extend(res)
					else:
						raise Exception("Impossible!! {}".format(str(e)))

			#print 'PLaying players after change', playing_players
			return playing_players




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
			self.conn.execute_query(query)

		#Once finished updating points of this round for all the players, we continue with the teams! 
		#Update teams points points_of_teams_by_round

		query = self.catalog.query_get_all_teams()		
		teams = self.conn.execute_query(query).fetchall()

		for team in teams:
			#Get players 
			team = Team(team[0], team[1:6], team[6:])
			players_ids = self.get_players_that_will_count(team, round_num)
			team_points = self.calculate_team_points(round_num, players_ids)

			query = self.catalog.query_update_team_points_for_round(round_num, team.key, team_points)
			self.conn.execute_query(query)
		return

	

if __name__ == '__main__':
	catalog = DefeCatalog()
	gdt = GranDT(catalog)

	gdt.init_db()

	gonza = Player('Gonza', 'delanteRo', 'SuperIOR')
	partu = Player('Partu', 'Defensor', 'Juveniles')
	mudo = Player('Mudo', 'defensor', 'menores')
	mono = Player('Mono', 'Arquero', 'menores')
	tebi = Player('Tebi', 'Arquero', 'Cadetes')
	nacho = Player('Nacho', 'delanteRo', 'superior')
	negro = Player('Negro', 'defensor', 'Juveniles')
	chola = Player('Chola', 'Defensor', 'Cadetes')
	seba = Player('Seba', 'delantero', 'Superior')


	gdt.add_player(gonza)
	gdt.add_player(partu)
	gdt.add_player(mudo)
	gdt.add_player(mono)
	gdt.add_player(tebi)
	gdt.add_player(nacho)
	gdt.add_player(negro)
	gdt.add_player(chola)
	gdt.add_player(seba)


	gdt.add_user(12, 'loco', 'locos', [  (gonza,1),
													(partu,0),
													(mudo,1),
													(mono,0),
													(tebi,1),
													(nacho,1),
													(negro,1),
													(chola,0),
													(seba,0)]
											)


#	gdt.change_team('b@a.com', [('Gonza','SuperIOR'),('Partu','Juveniles'),('Mudo','Menores'),('mono','menores'),('Tebi','cadetes')])
	
	#a = '{"round_number": 1212,"stats":[{ "name": "partu" ,"cat":"JuveNiLes" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}]}'
	a = '{"round_number": 1,"stats":[{ "name": "partu" ,"cat":"Juveniles" ,"pos": "Defensor" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "mudo" ,"cat":"menores" ,"pos": "defensor" ,"values": {"present": 0,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "gonza" ,"cat":"superior" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "mono" ,"cat":"menores" ,"pos": "arquero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "tebi" ,"cat":"cadetes" ,"pos": "arquero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "nacho" ,"cat":"superior" ,"pos": "delantero" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "negro" ,"cat":"JuveNiLes" ,"pos": "defensor" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "chola" ,"cat":"cadetes" ,"pos": "defensor" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}}, \
										{ "name": "seba" ,"cat":"superior" ,"pos": "delanteRo" ,"values": {"present": 1,"mvp": 1,"pen_goals": 1,"goals": 20,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 2,"blue_card": 1,"miss_pen": 3,"saved_pen": 1}} \
										]}'
	# a = {"number": 1, "stats": {"Superior": {"Gonza": {"present": 1,"absent": 1,"mvp": 1,"pen_goals": 1,"goals": 1,"against_goals": 1,"own_goals": 1,"yellow_card": 1,"red_card": 1,"blue_card": 1,"miss_pen": 1,"saved_pen": 1}}}}
	# a = json.dumps(a)
	gdt.add_round(a)