import unittest
from unittest.mock import MagicMock, patch, call
from gol import *

class GoLTest(unittest.TestCase):
    def test_init_dead(self):
        world = World()
        self.assertFalse(world.isAlive(Point(1,1)) )

    def test_should_alive_if_set(self):
        world = World()
        world.putLifeAt(Point(2,2))
        world.putLifeAt(Point(2,1))
        self.assertTrue(world.isAlive(Point(2,2)) )
        self.assertTrue(world.isAlive(Point(2,1)) )

    def test_should_dead_alone(self):
        world = World()
        world.putLifeAt(Point(2,2))
        newWorld = world.nextGen()
        self.assertFalse(newWorld.isAlive(Point(2,2)) )

    def test_should_alive_with_friends(self):
        world = World()
        world.putLifeAt(Point(1,1))
        world.putLifeAt(Point(1,0))
        world.putLifeAt(Point(1,2))
        newWorld = world.nextGen()
        self.assertTrue(newWorld.isAlive(Point(1,1)) )
    
    def test_get_3_around(self):
        world = World()
        world.putLifeAt(Point(1,1))
        world.putLifeAt(Point(0,0))
        world.putLifeAt(Point(1,0))
        world.putLifeAt(Point(2,2))
        self.assertEqual(3, world.around(Point(1,1)) )

    @patch('gol.World.around', MagicMock(return_value = 3))
    def test_should_alive_with_3_around(self):
        world = World()
        world.putLifeAt(Point(1,1))
        newWorld = world.nextGen()
        self.assertTrue(newWorld.isAlive(Point(1,1)) )

    @patch('gol.World.around', MagicMock(return_value = 4))
    def test_should_die_with_4_around(self):
        world = World()
        world.putLifeAt(Point(1,1))
        newWorld = world.nextGen()
        self.assertFalse(newWorld.isAlive(Point(1,1)) )

    @patch('gol.World.around', MagicMock(return_value = 2))
    def test_should_not_reproduce_with_2_around(self):
        world = World()
        newWorld = world.nextGen()
        self.assertFalse(newWorld.isAlive(Point(1,1)) )

    @patch('gol.World.willBeAlive')
    def test_should_check_all_alives_and_arounds_for_next_gen(self, mockChecker):
        mockChecker.return_value = False
        world = World()
        world.putLifeAt(Point(1,1))
        world.putLifeAt(Point(1,2))
        world.putLifeAt(Point(1,3))
        newWorld = world.nextGen()
        mockChecker.assert_has_calls( [call(Point(0,0)), call(Point(0,1)), call(Point(0,3)), \
                call(Point(1,1)), call(Point(1,2)), call(Point(1,3))], \
                any_order=True )

    def test_should_reproduce_with_3_around(self):
        world = World()
        world.putLifeAt(Point(1,1))
        world.putLifeAt(Point(1,2))
        world.putLifeAt(Point(1,3))
        newWorld = world.nextGen()
        self.assertTrue(newWorld.isAlive(Point(0,2)) )

    def test_word_output(self):
        world = World()
        world.putLifeAt(Point(1,1))
        world.putLifeAt(Point(2,2))
        world.putLifeAt(Point(1,3))
        expect = '''
....
.O.O
..O.
....'''
        self.assertEqual(expect, world.output(Point(0,0),Point(3,3)))

if __name__ == '__main__':
    unittest.main()
