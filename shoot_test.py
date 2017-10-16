import unittest
from unittest.mock import MagicMock
from unittest.mock import call
from shoot import Game, GameRecord, ShootRunner

class TestShootRunner(unittest.TestCase):
    
    def test_run_game(self):
        RECORD_STR = '共对决10次。刘备胜5次，胜率5%。曹操胜2次，胜率2%。吕布胜3次，胜率3%。'
        #given
        game = Game([('player1', 10), ('player2', 20)])
        runner = ShootRunner()
        mockRecord = MagicMock()
        runner.__createRecord__ = MagicMock(return_value = mockRecord)
        runner.run_round = MagicMock(side_effect = ['player1', 'player2', 'player2'])
        mockRecord.__str__.return_value = RECORD_STR
        #when
        actual = runner.run(3, game)
        #then
        self.assertEqual(RECORD_STR, actual)
        mockRecord.record.assert_has_calls([call('player1'), call('player2'), call('player2')])

    def test_record_str(self):
        #given
        game = Game([('刘备', 1), ('曹操', 2), ('吕布', 3)])
        record = GameRecord(game)
        #when
        for i in range(2): record.record('刘备')
        for i in range(1): record.record('曹操')
        for i in range(5): record.record('吕布')
        actual = record.__str__()
        #then
        expect = '''刘备命中率1%，曹操命中率2%，吕布命中率3%
对决8次。刘备胜2次，胜率25.0%；曹操胜1次，胜率12.5%；吕布胜5次，胜率62.5%。'''
        self.assertEqual(expect, actual)

    def test_run_round(self):
        #given
        game = Game([('player1', 0), ('player2', 100)])
        runner = ShootRunner()
        mockBattle = MagicMock()
        runner.__createBattle__ = MagicMock(return_value = mockBattle)
        mcokBattle.shoot.side_effect = lambda p1,p2: p2 == 'player2'
        #when
        actual = runner.run_round(game)
        #then
        mockBattle.shoot.assert_called_once_with('player1', 'player2')
        mockBattle.shoot.assert_called_once_with('player2', 'player1')
        self.assertEqual('player2', actual)
