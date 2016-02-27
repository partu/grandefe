import constants
import itertools

from table import Table


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

	def normalize(self, st):
		return st.title()

	#Checks
	def check_if_player_is_valid(self, position,category):
		assert  position in constants.ALLOWED_POSITIONS and category in constants.ALLOWED_CATEGORIES,  "Position ({}) or category ({}) is invalid".format(position,category)



	def check_if_team_is_valid(self, players_ids, categories):
		assert len(players_ids) == 5, "The amount of players you insert are different from 5."
		assert len(set(players_ids)) == 5, "You can't have the same player more than once"
		
		#Normalization		
		categories = [self.normalize(category) for category in categories]

		#Check if all categories are valid
		for category in categories:
			assert category in constants.ALLOWED_CATEGORIES, "Some player category isn't valid"

		#Check at least one of each category
		for category in constants.ALLOWED_CATEGORIES:
			assert category in categories, "You must have, at least, one player of each category"

	#queries
	def query_to_add_player(self, name, position, category):
		position = self.normalize(position)
		category = self.normalize(category)
		self.check_if_player_is_valid(position, category)
		return 'INSERT INTO players (nombre, posicion, categoria) VALUES ("{}","{}","{}")'.format(name, position, category)



	def query_to_add_user_and_team(self, email, user_name, team_name, players_ids, categories):
		self.check_if_team_is_valid(players_ids, categories)
		columns = [name for name, _type in self.users_teams().columns]
		query = 'INSERT INTO users_teams ({}) VALUES  ("{}","{}","{}",{})'.format(", ".join(columns), email, user_name, team_name, ",".join(str(pid) for pid in players_ids))
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



	def query_to_change_team(self, email, players_ids, categories):
		self.check_if_team_is_valid(players_ids, categories)
		columns = [name for name, _type in self.users_teams().columns if 'player' in name]
		col_values = list(itertools.chain(*zip(columns,players_ids)))
		col_values.append(email) #the email append is a really ugly hack
		query_template = 'UPDATE users_teams SET ' + '{}={},'*4 +'{}={} WHERE email = "{}"'
		query = query_template.format(*col_values)
		print query
		return query


	def query_get_player_id_by_name_and_category(self, name, category):
		name = self.normalize(name)
		category = self.normalize(category)
		query = 'SELECT player_id FROM players WHERE nombre = "{}" AND categoria = "{}"'.format(name, category)
		return query

	def query_to_check_valid_user(self, email):
		query = 'SELECT * FROM users_teams WHERE email = "{}"'.format(email)
		return query


	#TABLES
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
					('email','TEXT PRIMARY KEY'),
				    ('user_name','TEXT'),
				    ('team_name','TEXT'),
				    ('player1_id','INTEGER'),
				    ('player2_id','INTEGER'),
				    ('player3_id','INTEGER'),
				    ('player4_id','INTEGER'),
				    ('player5_id','INTEGER')
				   ]
		return Table(table_name, columns)

	def points_of_teams_by_round(self):
		table_name = 'points_of_team_by_round'
		columns = [
					('email','TEXT'),
					("round","INTEGER"), 
					("points","INTEGER"),
					("PRIMARY KEY", "(email, round)")
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