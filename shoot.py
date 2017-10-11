
class Game:
    def __init__(self, players):
        self.players = players

class GameRecord:
    def __init__(self, game):
        self.game = game
        self.times = 0
        self.wins = dict.fromkeys(map(lambda p: p[0], game.players), 0)
    def record(self, player):
        self.times += 1
        self.wins[player] = self.wins.get(player, 0) + 1
    def __str__(self):
        playerStr = map(lambda p: '{}命中率{:.0%}'.format(p[0], p[1]/100), self.game.players)
        result = '，'.join(playerStr)
        result += '\n对决{}次。刘备胜{}次，胜率100%；曹操胜0次，胜率0%；吕布胜0次，胜率0%。'.format(self.times, self.wins.get('刘备', 0))
        return result

class ShootRunner:
    def __createRecord__(self, game):
        return GameRecord(game)
    def run(self, times, game):
        record = self.__createRecord__(game)
        record.record('player1')
        return record.__str__()

def main():
    game = Game([('刘备', 30), ('曹操', 50), ('吕布', 100)])
    runner = ShootRunner()
    print(runner.run(10, game))

if __name__ == '__main__':
    main()
