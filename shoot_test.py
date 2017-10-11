import unittest
from unittest.mock import MagicMock
from shoot import Game, GameRecord, ShootRunner

class TestShootRunner(unittest.TestCase):
    
    def test_run_game(self):
        #given
        RECORD_STR = '共对决10次。刘备胜5次，胜率5%。曹操胜2次，胜率2%。吕布胜3次，胜率3%。'
        game = Game([('player1', 10), ('player2', 20)])
        runner = ShootRunner()
        mockRecord = MagicMock()
        runner.__createRecord__ = MagicMock(return_value = mockRecord)
        mockRecord.__str__.return_value = RECORD_STR
        #when
        actual = runner.run(10, game)
        #then
        self.assertEqual(RECORD_STR, actual)
        mockRecord.record.assert_called_with('player1')

    def test_record_str(self):
        #given
        game = Game([('刘备', 1), ('曹操', 2), ('吕布', 3)])
        record = GameRecord(game)
        #when
        record.record('刘备')
        record.record('刘备')
        actual = record.__str__()
        #then
        expect = '''刘备命中率1%，曹操命中率2%，吕布命中率3%
对决2次。刘备胜2次，胜率100%；曹操胜0次，胜率0%；吕布胜0次，胜率0%。'''
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
