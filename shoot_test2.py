import unittest
from shoot2 import *

class TestShoot(unittest.TestCase):
    def test_one_game_result(self):
        actual = repeatRun([('p1', 30), ('p2', 50)],1)
        expect = '''Game Info: p1 rate:30, p2 rate:50.
run 1 times: 
p1 win 0 times, 0%;
p2 win 1 times, 100%'''
        self.assertEqual(expect, actual.__str__())
        self.assertEqual(1, len(actual.games))
        self.assertEqual('p2', actual.games[0].winner)

    def test_2_player_p1_win_at_1st_shoot(self):
        game = runGame([('p1', 100), ('p2', 0)])
        self.assertEqual('p1', game.winner)

if __name__ == '__main__':
    unittest.main()




