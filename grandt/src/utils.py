import collections

#namedtuplesha
Player = collections.namedtuple('Player',['name', 'position', 'category'])
Team = collections.namedtuple('Team',['key', 'titulars', 'alternates'])
TeamInfo = collections.namedtuple('TeamInfo', ['dni', 'user_name', 'team_name', 'tit1', 'tit2', 'tit3','tit4','tit5','sup1','sup2','sup3','sup4'])
