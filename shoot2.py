def repeatRun(players, times):
    results =  GameResults()
    results.games.append(runGame(players))
    return results

def runGame(players):
    game = Game()
    if shoot(players[0], players[1]):
        game.winner = 'p1'    
    else:
        game.winner = 'p2'
    return game

def shoot(p1, p2):
    return True

class Game:
    def __init__(self):
        self.winner = None

class GameResults:
    def __init__(self):
        self.games = []
    def __str__(self):
        return '''Game Info: p1 rate:30, p2 rate:50.
run 1 times: 
p1 win 0 times, 0%;
p2 win 1 times, 100%'''

if __name__ == '__main__':
    print( repeatRun([], 10) )

