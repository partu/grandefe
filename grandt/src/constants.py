
DB_NAME = 'defe_gdt.db'


#Positions
ARQUERO = 'Arquero'
DEFENSOR =  'Defensor'
#MEDIOCAMPISTA =   'Mediocampista'
DELANTERO =  'Delantero'

ALLOWED_POSITIONS  = {ARQUERO,DEFENSOR,DELANTERO}


#Categories
MENORES = 'Menores'
CADETES =  'Cadetes'
JUVENILES = 'Juveniles'
SUPERIOR ='Superior'

ALLOWED_CATEGORIES  = {MENORES,CADETES,JUVENILES,SUPERIOR}



#NUMBERS
NUMBER_OF_TITULARS = 5
NUMBER_OF_ALTERNATES = 4
NUMBER_OF_PLAYERS_IN_TEAM = 9



#JSON format
ROUND_NUMBER = "round_number"
STATS = "stats"
NAME  = "name"
CATEGORY  = "cat"
POSITION = "pos"
VALUES = "values"


#ACTIONS
ACT_PRESENT = "present"
ACT_MVP = "mvp"
ACT_PEN_GOALS = "pen_goals"
ACT_GOALS = "goals"
ACT_AGAINST_GOALS = "against_goals"
ACT_OWN_GOALS = "own_goals"
ACT_YELLOW_CARD = "yellow_card"
ACT_RED_CARD = "red_card"
ACT_BLUE_CARD = "blue_card"
ACT_MISS_PEN = "miss_pen"
ACT_SAVED_PEN = "saved_pen"


ACTIONS = [ACT_PRESENT,ACT_MVP,ACT_PEN_GOALS,ACT_GOALS,ACT_AGAINST_GOALS,ACT_OWN_GOALS,ACT_YELLOW_CARD,ACT_RED_CARD,ACT_BLUE_CARD,ACT_MISS_PEN,ACT_SAVED_PEN]

ACTIONS_POINTS = \
	{	
		ARQUERO:{
					ACT_PRESENT:"0",
					ACT_MVP: "4",
					ACT_PEN_GOALS: "3",
					ACT_GOALS: "10",
					ACT_AGAINST_GOALS: "-1",
					ACT_OWN_GOALS: "-2",
					ACT_YELLOW_CARD: "-2",
					ACT_RED_CARD: "-8",
					ACT_BLUE_CARD: "-4",
					ACT_MISS_PEN: "-4",
					ACT_SAVED_PEN: "4"
				},
		DEFENSOR:{
					ACT_PRESENT:"0",
					ACT_MVP: "4",
					ACT_PEN_GOALS: "3",
					ACT_GOALS: "8",
					ACT_AGAINST_GOALS:"0",
					ACT_OWN_GOALS: "-2",
					ACT_YELLOW_CARD: "-2",
					ACT_RED_CARD: "-8",
					ACT_BLUE_CARD: "-4",
					ACT_MISS_PEN: "-4",
					ACT_SAVED_PEN: "4"
				},
		DELANTERO:{
					ACT_PRESENT:"0",
					ACT_MVP: "4",
					ACT_PEN_GOALS: "3",
					ACT_GOALS: "4",
					ACT_AGAINST_GOALS:"0",
					ACT_OWN_GOALS: "-2",
					ACT_YELLOW_CARD: "-2",
					ACT_RED_CARD: "-8",
					ACT_BLUE_CARD: "-4",
					ACT_MISS_PEN: "-4",
					ACT_SAVED_PEN: "4"
				}
		}