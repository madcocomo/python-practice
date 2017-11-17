import unittest
from shoot2 import *

class TestShoot(unittest.TestCase):
    def test_one_game_result(self):
        actual = runGame([('p1', 30), ('p2', 50)],1)
        expect = '''Game Info: p1 rate:30, p2 rate:50.
run 1 times: 
p1 win 0 times, 0%;
p2 win 1 times, 100%'''
        self.assertEqual(expect, actual.__str__())
        self.assertEqual('p2', actual.games[0].winner)

if __name__ == '__main__':
    unittest.main()




