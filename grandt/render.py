from argparse import ArgumentParser
from src.utils import Player
from src.ui.templates import players_template, teams_points_template, teams_template, player_points_template, mapping_points_template
from src.granDT import GranDT
from src.catalog import DefeCatalog
from src.constants import ACTIONS_COMPLETE_NAME_SPANISH

class Shower(object):
	def __init__(self):
		self.catalog = DefeCatalog()
		self.granDT = GranDT(self.catalog)


	def show_players(self):
		players = self.granDT.get_players()
		t = players_template
		
		with open('players.html','w')  as f:
			f.write(t.render(players=players))

	def show_teams(self):
		teams = self.granDT.get_teams()
		t = teams_template
		
		with open('teams.html','w')  as f:
			f.write(t.render(teams=teams))


	def show_teams_points(self):
		teams_points = self.granDT.get_teams_points()
		played_rounds = len(teams_points.itervalues().next()) -1 #To leave space for the TOTAL column
		t = teams_points_template
		
		with open('teams_points.html','w')  as f:
			f.write(t.render(teams_points=sorted(teams_points.items(), key=lambda (key,value): value[-1][1], reverse=True), rounds=played_rounds))


	def show_player_points(self,player_name):
		player, player_points = self.granDT.get_player_stats(player_name)
		played_rounds = len(player_points) -1 #To leave space for the TOTAL column
		t = player_points_template

		with open('player_points.html','w')  as f:
			f.write(t.render(player_points=player_points, rounds=played_rounds, player= player))


	def show_mapping_points(self):
		mapping = self.granDT.get_mapping_points()
		t = mapping_points_template
		with open('mapping_points.html','w')  as f:
			f.write(t.render(column_names_spanish=ACTIONS_COMPLETE_NAME_SPANISH, mapping= mapping))








if __name__ == '__main__':

	parser = ArgumentParser()
	parser.add_argument('-t',dest='task', choices=['PlayerPoints', 'TeamPoints', 'Teams', 'Players', 'MappingPoints'] , help="Task to be done.")
	parser.add_argument('-n',dest='name',nargs='+', help="If PlayerPoints option has been choosen, enter the name of the player here.")

	args = parser.parse_args()

	shower = Shower()

	if not args.task:
		parser.error('Missing arguments')

	filename_written = None

	if args.task == 'PlayerPoints':
		if not args.name:
			parser.error("Missing name of the player")
		shower.show_player_points(" ".join(args.name))
		filename_written = 'player_points.html'
	elif args.task == 'TeamPoints':
		shower.show_teams_points()
		filename_written = 'teams_points.html'
	elif args.task == 'Teams':
		shower.show_teams()
		filename_written = 'teams.html'
	elif args.task == 'Players':
		shower.show_players()
		filename_written = 'players.html'
	elif args.task == 'MappingPoints':
		shower.show_mapping_points()
		filename_written = 'mapping_points.html'

	print 'Task accomplished. The output file is: {}'.format(filename_written)
