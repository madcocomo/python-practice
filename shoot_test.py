import unittest
from unittest.mock import MagicMock
from shoot import Game, GameRecord, ShootRunner

class TestShootRunner(unittest.TestCase):
	
	def test_run_game(self):
		#given
		RECORD_STR = '共对决10次。刘备胜5次，胜率5%。曹操胜2次，胜率2%。吕布胜3次，胜率3%。'
		game = Game()
		runner = ShootRunner()
		stubRecord = MagicMock()
		runner.__createRecord__ = MagicMock(return_value = stubRecord)
		stubRecord.__str__.return_value = RECORD_STR
		#when
		actual = runner.run(10, game)
		#then
		self.assertEqual(RECORD_STR, actual)

	def test_record_str(self):
		game = MagicMock()
		record = GameRecord(game)
		actual = record.__str__()
		self.assertEqual('对决信息：刘备命中率1%，曹操命中率2%，吕布命中率3%', actual)


if __name__ == '__main__':
	unittest.main()
