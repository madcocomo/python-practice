
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
        self.wins[player] += 1
    def playersInfo(self):
        playerStr = map(lambda p: '{}命中率{:.0%}'.format(p[0], p[1]/100), self.game.players)
        return '，'.join(playerStr)
    def gameInfo(self):
        gameStr = map(lambda winner: '{}胜{}次，胜率{:.0%}'.format(winner[0], winner[1], winner[1]/self.times), self.wins.items())
        return '对决{}次。'.format(self.times) + '；'.join(gameStr) + "。"
    def __str__(self):
        return self.playersInfo() + '\n' + self.gameInfo()

class ShootRunner:
    def __createRecord__(self, game):
        return GameRecord(game)
    def run(self, times, game):
        record = self.__createRecord__(game)
        record.record(game.players[0][0])
        return record.__str__()

def main():
    game = Game([('刘备', 30), ('曹操', 50), ('吕布', 100)])
    runner = ShootRunner()
    print(runner.run(10, game))

if __name__ == '__main__':
    main()
