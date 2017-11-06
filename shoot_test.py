import unittest
from unittest.mock import MagicMock, call, patch
from shoot import Game, GameRecord, ShootRunner, Battle, Player

class TestShootRunner(unittest.TestCase):
    @patch('shoot.Battle.run')
    @patch('shoot.GameRecord')
    def test_run_game(self, recordCreater, mockRun):
        RECORD_STR = '共对决10次。刘备胜5次，胜率5%。曹操胜2次，胜率2%。吕布胜3次，胜率3%。'
        #given
        game = Game([('player1', 10), ('player2', 20)])
        runner = ShootRunner(game)
        mockRecord = recordCreater.return_value
        mockRecord.__str__.return_value = RECORD_STR
        mockRun.side_effect = ['player1', 'player2', 'player2']
        #when
        actual = runner.run(3)
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

    @patch('shoot.Battle.run')
    def test_run_battle(self, mockRun):
        #given
        game = Game([('player1', 0), ('player2', 100)])
        runner = ShootRunner(game)
        mockRun.return_value='player2'
        #when
        actual = runner.run_battle()
        #then
        mockRun.assert_called_once_with()
        self.assertEqual('player2', actual)

    @patch('shoot.Game.isHit')
    def test_one_round_battle(self,mockHit):
        #given
        mockHit.side_effect = lambda shooter: shooter.name == 'player2'
        game = Game([('player1', 0), ('player2', 100)])
        battle = Battle(game)
        #when
        winner = battle.run()
        #then
        self.assertEqual('player2', winner)
        round1 = battle.rounds[0]
        self.assertEqual(('player1', 'player2', False), round1.log[0])
        self.assertEqual(('player2', 'player1', True), round1.log[1])
        mockHit.assert_has_calls([call(Player('player1',0)), call(Player('player2',100))])

    @patch('shoot.Game.isHit')
    def test_two_round_battle(self, mockHit):
        #given
        player1 = Player('player1', 0)
        player2 = Player('player2', 50)
        game = Game([('player1', 0), ('player2', 50)])
        battle = Battle(game)
        mockHit.side_effect = [False, False, False, True]
        #when
        winner = battle.run()
        #then
        self.assertEqual('player2', winner)
        round1 = battle.rounds[0]
        self.assertEqual(('player1', 'player2', False), round1.log[0])
        self.assertEqual(('player2', 'player1', False), round1.log[1])
        round2 = battle.rounds[1]
        self.assertEqual(('player1', 'player2', False), round2.log[0])
        self.assertEqual(('player2', 'player1', True), round2.log[1])
        mockHit.assert_has_calls([call(player1), call(player2), call(player1), call(player2)])

    @patch('shoot.Game.isHit', MagicMock(return_value = True))
    def test_battle_finished_middle_of_round(self):
        #given
        game = Game([('player1', 0), ('player2', 50)])
        battle = Battle(game)
        #when
        winner = battle.run()
        #then
        self.assertEqual('player1', winner)
        self.assertEqual(1, len(battle.rounds))
        round1 = battle.rounds[0]
        self.assertEqual(1, len(round1.log))
        self.assertEqual(('player1', 'player2', True), round1.log[0])
        game.isHit.assert_called_once_with(Player('player1',0))

    @patch('shoot.Game.isHit', MagicMock(return_value = False))
    def test_should_not_endless_running_round(self):
        #given
        game = Game([('player1', 0), ('player2', 0)])
        battle = Battle(game)
        #when
        with self.assertRaises(Exception) as context:
            winner = battle.run()
        #then
        self.assertTrue('dead loop' in str(context.exception))

    def test_game_isHit(self):
        player1 = Player('player1', 30)
        game = Game([('player1', 30), ('player2', 0)])
        hitCount = 0
        testCount = 100000
        ideaHit = testCount * 30/100
        for i in range(testCount):
            if game.isHit(player1): hitCount+=1
        self.assertTrue(hitCount < ideaHit + testCount * 0.003, 'hit too high {}'.format(hitCount))
        self.assertTrue(hitCount > ideaHit - testCount * 0.003, 'miss too high {}'.format(hitCount))

    def test_select_highest_rate_target(self):
        #given
        shooter = Player('shooter', 100)
        player1 = Player('player1', 80)
        player2 = Player('player2', 50)

        #when
        target = shooter.chooseTarget([player1, player2, shooter])
        #then
        self.assertEqual(player1.name, target.name)
        

if __name__ == '__main__':
    unittest.main()

