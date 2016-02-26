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
	def __init__(self):
		self.db_name = 'defe_gdt.db'
		super(DefeCatalog,self).__init__(self.db_name)


	def initialize(self):
		self.add_table(self.history_of_players_by_date())
		self.add_table(self.users())
		self.add_table(self.teams())
		self.add_table(self.players())


	#tables
	def history_of_players_by_date(self):
		table_name = 'history'
		columns = [
					("player_id","INTEGER"),
					("round","INTEGER"), 
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
					("PRIMARY KEY", "(player_id, round)")
				]
		return Table(table_name, columns)

	def users(self):
		table_name = 'users'
		columns = [
					('email', 'TEXT PRIMARY KEY'),
				    ('user_name','TEXT'),
				    ('team_name','TEXT')
				  ]
		return Table(table_name, columns)


	def teams(self):
		table_name = 'teams'			
		columns =  [
					('user_id','INTEGER'),
				    ('team_name','TEXT'),
				    ('player1_id','INTEGER'),
				    ('player2_id','INTEGER'),
				    ('player3_id','INTEGER'),
				    ('player4_id','INTEGER'),
				    ('player5_id','INTEGER')
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