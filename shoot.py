
class Game:
    def __init__(self, players):
        self.players = players

class BattleRound:
    def __init__(self, players):
        self.log = []
        self.aliver = list(players)
    def run(self):
        self.log.append((self.aliver[0][0], self.aliver[1][0], False))
        self.log.append((self.aliver[1][0], self.aliver[0][0], True))
        del self.aliver[0]

class Battle:
    def __init__(self, game):
        self.game = game
        self.rounds = []
    def run(self):
        newRound = BattleRound(self.game.players)
        self.rounds.append(newRound)
        newRound.run()
        if len(newRound.aliver) == 1:
            return newRound.aliver[0][0]
        return newRound.aliver[0][0]

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
        gameStr = map(lambda p: '{}胜{}次，胜率{:.1%}'.format(p[0], self.wins[p[0]], self.wins[p[0]]/self.times), self.game.players)
        return '对决{}次。'.format(self.times) + '；'.join(gameStr) + "。"
    def __str__(self):
        return self.playersInfo() + '\n' + self.gameInfo()

class ShootRunner:
    def __init__(self, game):
        self.game = game
    def __createRecord__(self):
        return GameRecord(self.game)
    def __createBattle__(self):
        return Battle(self.game)
    def run_battle(self):
        return self.__createBattle__().run()
    def run(self, times):
        record = self.__createRecord__()
        for i in range(times):
            record.record(self.run_battle())
        return record.__str__()

def main():
    game = Game([('刘备', 30), ('曹操', 50), ('吕布', 100)])
    runner = ShootRunner(game)
    print(runner.run(10))

if __name__ == '__main__':
    main()
