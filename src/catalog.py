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
		assert self.normalize(player.position) in constants.ALLOWED_POSITIONS and self.normalize(player.category) in constants.ALLOWED_CATEGORIES,  "Position ({}) or category ({}) is invalid".format(position,category)



	def check_if_team_is_valid(self, players_info):
		players_ids = [player_id for player_id, category, titularity in players_info]
		alternate_players_info = filter(lambda p_info: p_info[2] == 0, players_info)
		titular_players_info = set(players_info) - set(alternate_players_info)

		assert len(players_ids) == 9, "The amount of players you insert are different from 9."
		assert len(set(players_ids)) == 9, "You can't have the same player more than once"
		assert len(alternate_players_info) == 4, "There must exists exactly 4 alternate players"
		assert len(titular_players_info) == 5, "There must exists exactly 5 titular players"

		#Check if all categories are valid
		for _, player, _ in players_info:
			assert self.normalize(player.category) in constants.ALLOWED_CATEGORIES, "Category {} is invalid".format(self.normalize(self.normalize(player.category)))

		#Check one alternate player per position
		alternate_positions = {self.normalize(player.position) for _, player, _ in alternate_players_info}
		assert alternate_positions == set(constants.ALLOWED_POSITIONS), "You must have one alternate player per each position" 

		#check tactic



	#queries
	def query_to_add_player(self, player):
		self.check_if_player_is_valid(player)
		return 'INSERT INTO players (nombre, posicion, categoria) VALUES ("{}","{}","{}")'.format(self.normalize(player.name), self.normalize(player.position), self.normalize(player.category))



	def query_to_add_user_and_team(self, dni, user_name, team_name, players_info):
		''' Each player info is a 3-tuple of id, Player and if it's titular or not '''
		self.check_if_team_is_valid(players_info)
		players_ids = [pid for pid, _ , _  in players_info ]
		columns = [name for name, _type in self.users_teams().columns]
		query = 'INSERT INTO users_teams ({}) VALUES  ("{}","{}","{}",{})'.format(", ".join(columns), dni, user_name, team_name, ",".join(str(pid) for pid in players_ids))
		return query


	def query_to_add_player_statistics_of_round(self, _round, player_id, stats):
		''' stats is a dictionary where the keys are the same of the columns in the table 'history' '''
		columns = [name for name, _type in self.history_of_players_by_round().columns]

		values = [_round, player_id]
		for name in columns:
			if name not in ('round','player_id'):
				values.append(stats[name])


		query = 'INSERT INTO history ({}) VALUES ({})'.format(", ".join(columns), ", ".join(values))
		print query



	def query_to_change_team(self, dni, players_ids, categories):
		self.check_if_team_is_valid(players_ids, categories)
		columns = [name for name, _type in self.users_teams().columns if 'player' in name]
		col_values = list(itertools.chain(*zip(columns,players_ids)))
		col_values.append(dni) #the dni append is a really ugly hack
		query_template = 'UPDATE users_teams SET ' + '{}={},'*4 +'{}={} WHERE dni = "{}"'
		query = query_template.format(*col_values)
		print query
		return query


	def query_get_player_id_by_name_and_category(self, player):
		query = 'SELECT player_id FROM players WHERE nombre = "{}" AND categoria = "{}"'.format(self.normalize(player.name), self.normalize(player.category))
		return query

	def query_to_check_valid_user(self, dni):
		query = 'SELECT * FROM users_teams WHERE dni = "{}"'.format(dni)
		return query


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
					("present","INTEGER"), 
					("absent","INTEGER"), 
					("mvp","INTEGER"), 
					("pen_goals","INTEGER"), 
					("goals","INTEGER"), 
					("against_goals","INTEGER"), 
					("own_goals","INTEGER"), 
					("yellow_card","INTEGER"), 
					("red_card","INTEGER"), 
					("blue_card","INTEGER"), 
					("miss_pen","INTEGER"), 
					("saved_pen","INTEGER"),
					("total_points","INTEGER"),
					("PRIMARY KEY", "(player_id, round)")
				]
		return Table(table_name, columns)

	def users_teams(self):
		table_name = 'users_teams'			
		columns =  [
					('dni','INTEGER PRIMARY KEY'),
				    ('user_name','TEXT'),
				    ('team_name','TEXT'),
				    ('player1_id','INTEGER'),
				    ('player2_id','INTEGER'),
				    ('player3_id','INTEGER'),
				    ('player4_id','INTEGER'),
				    ('player5_id','INTEGER'),
				    ('player6_id','INTEGER'),
				    ('player7_id','INTEGER'),
				    ('player8_id','INTEGER'),
				    ('player9_id','INTEGER')
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
				    ('nombre','TEXT'),
				    ('posicion','TEXT'),
				    ('categoria','TEXT')
				  ]
		return Table(table_name, columns)