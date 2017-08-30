
class Game:
	pass

class GameRecord:
	def __init__(self, game):
		pass

class ShootRunner:
	def __createRecord__(self, game):
		return GameRecord(game)
	def run(self, times, game):
		return self.__createRecord__(game).__str__()
