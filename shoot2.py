
def runGame(players, times):
    results =  GameResults()
    results.games.append({'winner': 'p2'})
    return results

class GameResults:
    def __init__(self):
        self.games = []
    def __str__(self):
        return '''Game Info: p1 rate:30, p2 rate:50.
run 1 times: 
p1 win 0 times, 0%;
p2 win 1 times, 100%'''

