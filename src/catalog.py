import constants
import itertools
import collections
from table import Table

Player = collections.namedtuple('Player',['name', 'position', 'category'])


class Catalog(object):
	def __init__(self, db_name):
		self.db_name = db_name
		self.tables = []


	def db_name(self):
		return self.db_name

	def table_names(self):
		return [table.name for table in self.tables] 

	def add_table(self, table):
		self.tables.append(table)

	def tables(self):
		return self.tables


class DefeCatalog(Catalog):
	def __init__(self, db_name=None):
		self.db_name = db_name or constants.DB_NAME
		super(DefeCatalog,self).__init__(self.db_name)
		self.add_table(self.history_of_players_by_round())
		self.add_table(self.users_teams())
		self.add_table(self.players())
		self.add_table(self.points_of_teams_by_round())
		self.add_table(self.points_of_action_by_position())

	def normalize(self, st):
		return st.title()

	#Checks
	def check_if_player_is_valid(self, player):
		assert self.normalize(player.position) in constants.ALLOWED_POSITIONS and self.normalize(player.category) in constants.ALLOWED_CATEGORIES,  "Position ({}) or category ({}) is invalid".format(player.position,player.category)



	def check_if_team_is_valid(self, players_info):
		players_ids = [player_id for player_id, category, titularity in players_info]
		alternate_players_info = filter(lambda p_info: p_info[2] == 0, players_info)
		titular_players_info = set(players_info) - set(alternate_players_info)

		#Check amount of titulars and alterantes
		assert len(players_ids) == constants.NUMBER_OF_PLAYERS_IN_TEAM, "The amount of players you insert are different from {}.".format(constants.NUMBER_OF_PLAYERS_IN_TEAM)
		assert len(set(players_ids)) == constants.NUMBER_OF_PLAYERS_IN_TEAM, "You can't have the same player more than once"
		assert len(alternate_players_info) == constants.NUMBER_OF_ALTERNATES, "There must exists exactly {} alternate players".format(constants.NUMBER_OF_ALTERNATES)
		assert len(titular_players_info) == constants.NUMBER_OF_TITULARS, "There must exists exactly {} titular players".format(constants.NUMBER_OF_TITULARS)

		#Check if all categories and positions are valid
		for _, player, _ in players_info:
			self.check_if_player_is_valid(player)

		#Check positions and categories for alternate players
		alternate_positions = {self.normalize(player.position) for _, player, _ in alternate_players_info}
		alternate_categories = {self.normalize(player.category) for _, player, _ in alternate_players_info}
		assert alternate_positions == constants.ALLOWED_POSITIONS, "You must have one alternate player per each position at least" 
		assert alternate_categories == constants.ALLOWED_CATEGORIES, "You must have one alternate player per category"

		#Check positions and categories for titular players
		titulars_positions =  [self.normalize(player.position) for _, player, _ in titular_players_info]
		titulars_categories = [self.normalize(player.category) for _, player, _ in titular_players_info]
		assert titulars_positions.count(constants.ARQUERO) == 1, "You must have only one goalkeeper inside your titular team"
		assert titulars_positions.count(constants.DEFENSOR) == 2, "You must have only two defenses inside your titular team"
		assert titulars_positions.count(constants.DELANTERO) == 2, "You must have only two offenser inside your titular team"
		assert set(titulars_categories) == constants.ALLOWED_CATEGORIES, "You must have at least one player of each category inside your titular team"
		assert titulars_categories.count(constants.SUPERIOR) == 2, "You must two players of each {} category inside your titular team".format(constants.SUPERIOR)





	#queries
	def queries_for_init(self):
		queries = []
		table_columns = self.points_of_action_by_position().format_columns_for_insert_query()
		hack_act = '"{act}"'
		hack_pos = '"{pos}"'
		hack_pts = '{pts}'

		query_template = 'INSERT INTO points_of_action_by_position ({columns}) VALUES ({act},{pos},{pts})'.format(columns=table_columns,act=hack_act, pos=hack_pos, pts=hack_pts) #hacks

		for position in constants.ACTIONS_POINTS.keys():
			for action in constants.ACTIONS:
				points = constants.ACTIONS_POINTS[position][action]
				query = query_template.format(act=action, pos=position, pts=points)
				queries.append(query)
		return	queries



	def query_to_add_player(self, player):
		self.check_if_player_is_valid(player)
		query = 'INSERT INTO players (name, position, category) VALUES ("{}","{}","{}")'
		return query.format(self.normalize(player.name), self.normalize(player.position), self.normalize(player.category))


	def query_to_add_user_and_team(self, dni, user_name, team_name, players_info):
		''' Each player info is a 3-tuple of id, Player and if it's titular or not '''
		self.check_if_team_is_valid(players_info)
		#put the titulars at the beginning
		players_info = sorted(players_info, key=lambda p_info: p_info[2], reverse=True)
		
		players_ids = [pid for pid, _ , _  in players_info ]
		columns = [name for name, _type in self.users_teams().columns]
		query = 'INSERT INTO users_teams ({}) VALUES  ("{}","{}","{}",{})'.format(", ".join(columns), dni, user_name, team_name, ",".join(str(pid) for pid in players_ids))
		return query

	def query_to_change_team(self, dni, players_ids, categories):
		self.check_if_team_is_valid(players_ids, categories)
		columns = [name for name, _type in self.users_teams().columns if 'player' in name]
		col_values = list(itertools.chain(*zip(columns,players_ids)))
		col_values.append(dni) #the dni append is a really ugly hack
		query_template = 'UPDATE users_teams SET ' + '{}={},'*4 +'{}={} WHERE dni = "{}"'
		query = query_template.format(*col_values)
		return query


	def query_to_set_history_entry(self, round_num, player_id, total_points, player_values):
		query_template = "INSERT INTO history ({cols}) VALUES ({rnd},{id},{pts},{vals})"
		cols = self.history_of_players_by_round().format_columns_for_insert_query()

		#Put them in the same order
		#HACK!!!CHANGE THIS! 
		_values = [player_values[col_name.strip()] for col_name in cols.split(',') if col_name.strip() not in ('round','player_id','total_points') ] 


		query = query_template.format(cols=cols, rnd=round_num, id=player_id, pts=total_points, vals=",".join(str(val) for val in _values)) 
		return query 

	def query_get_positions_of_players(self, players_ids):
		query = 'SELECT player_id, position FROM players WHERE player_id IN ({ids})'
		return query.format(ids=",".join(str(_id) for _id in players_ids))



	def query_get_all_teams(self):
		query = 'SELECT dni, tit1_id,tit2_id,tit3_id,tit4_id,tit5_id,sup1_id,sup2_id,sup3_id,sup4_id FROM users_teams'
		return query

	def query_get_player_id_by_name_category_and_position(self, player):
		query = 'SELECT player_id FROM players WHERE name = "{}" AND category = "{}" AND position = "{}"'
		return query.format(self.normalize(player.name), self.normalize(player.category), self.normalize(player.position))

	def query_to_check_valid_user(self, dni):
		query = 'SELECT * FROM users_teams WHERE dni = "{}"'
		return query.format(dni)

	def query_all_actions_points_for_position(self, position):
		query = 'SELECT action, points FROM points_of_action_by_position WHERE position = "{}"'
		return query.format(self.normalize(position))

	def query_get_if_present_players_and_positions(self, _round, players_ids):
		query = 'SELECT p.player_id, p.position, h.{present}  FROM history h, players p WHERE h.player_id IN ({ids}) AND h.player_id = p.player_id AND h.round = {round}'
		return query.format(round=_round, present=constants.ACT_PRESENT, ids=",".join(str(_id) for _id in players_ids))

	def get_points_for_player_id_in_round(self, round_num, players_ids):
		query = 'SELECT player_id, total_points FROM history WHERE round = {round} AND player_id IN ({ids})'
		return query.format(round= round_num, ids=','.join(str(_id) for _id in players_ids))

	def query_update_team_points_for_round(self, round_num, team_key, team_points):
		query = 'INSERT INTO points_of_team_by_round ({columns}) VALUES ({_values})'
		columns = self.points_of_teams_by_round().format_columns_for_insert_query()
		_values = [team_key, round_num, team_points]
		return query.format(columns=columns, _values=",".join(str(x) for x in _values ))


	#TABLES
	def points_of_action_by_position(self):
		table_name = 'points_of_action_by_position'
		columns = [  ("action", "TEXT"),
					 ("position", "TEXT"),
					 ("points", "INTEGER"),
					 ("PRIMARY KEY", "(action,position)")
			       ]

		return Table(table_name, columns)

	def history_of_players_by_round(self):
		table_name = 'history'
		columns = [
					("round","INTEGER"), 
					("player_id","INTEGER"),
					("total_points","INTEGER"),
				]
		actions = [(action, "INTEGER") for action in constants.ACTIONS]
		columns.extend(actions)
		columns.append(("PRIMARY KEY", "(player_id, round)"))

		return Table(table_name, columns)

	def users_teams(self):
		table_name = 'users_teams'			
		columns =  [
					('dni','INTEGER PRIMARY KEY'),
				    ('user_name','TEXT'),
				    ('team_name','TEXT'),
				    ('tit1_id','INTEGER'),
				    ('tit2_id','INTEGER'),
				    ('tit3_id','INTEGER'),
				    ('tit4_id','INTEGER'),
				    ('tit5_id','INTEGER'),
				    ('sup1_id','INTEGER'),
				    ('sup2_id','INTEGER'),
				    ('sup3_id','INTEGER'),
				    ('sup4_id','INTEGER')
				   ]
		return Table(table_name, columns)

	def points_of_teams_by_round(self):
		table_name = 'points_of_team_by_round'
		columns = [
					('dni','INTEGER'),
					("round","INTEGER"), 
					("points","INTEGER"),
					("PRIMARY KEY", "(dni, round)")
				  ]
		return Table(table_name, columns)


	def players(self):
		table_name = 'players'
		columns = [
					('player_id','INTEGER PRIMARY KEY ASC'),
				    ('name','TEXT'),
				    ('position','TEXT'),
				    ('category','TEXT')
				  ]
		return Table(table_name, columns)