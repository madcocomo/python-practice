import random
from random import randint

#TODO Player object

class Game:
    def __init__(self, players):
        self.players = players
    def isHit(self, shooter):
        player = list(filter(lambda p: p[0]==shooter, self.players))[0]
        return randint(1,100) <= player[1]

class BattleRound:
    def __init__(self, players, game):
        self.log = []
        self.alivers = list(players)
        self.game = game
    def run(self):
        for player in self.alivers:
            if len(self.alivers) == 1: return
            self.shoot(player[0], self.chooseTarget(player)[0])
    def chooseTarget(self, player):           
        if player == self.alivers[-1]: return self.alivers[-2]
        return self.alivers[-1]
    def shoot(self, shooter, target):
        isHit = self.game.isHit(shooter)
        self.log.append((shooter, target, isHit))
        if isHit:
            self.die(target)
    def die(self, playerName):
        for player in self.alivers:
            if (player[0] == playerName):
                dead = player
        self.alivers.remove(dead)
        
class Battle:
    def __init__(self, game):
        self.game = game
        self.rounds = []
    def run(self):
        alivers = self.game.players
        #while len(alivers) > 1:
        for time in range(100):
            if len(alivers) == 1:
                return alivers[0][0]
            newRound = BattleRound(alivers, self.game)
            self.rounds.append(newRound)
            newRound.run()
            alivers = newRound.alivers
        raise Exception('dead loop')

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
    print(runner.run(100))

if __name__ == '__main__':
    main()
