import random
from random import randint

class Player:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
    def chooseTarget(self, alivers):           
        alivers = sorted(alivers, key=lambda p:p.rate)
        if self == alivers[-1]: return alivers[-2]
        return alivers[-1]
    def __str__(self):
        return '{}命中率{:.0%}'.format(self.name, self.rate/100)
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class Game:
    def __init__(self, players):
        self.players = list(map(lambda p: Player(*p), players))
    def isHit(self, shooter):
        player = shooter
        return randint(1,100) <= player.rate

class BattleRound:
    def __init__(self, players, game):
        self.log = []
        self.alivers = list(players)
        self.game = game
    def run(self):
        for player in self.alivers:
            if len(self.alivers) == 1: return
            self.shoot(player)
    def shoot(self, shooter):
        target = shooter.chooseTarget(self.alivers)
        isHit = self.game.isHit(shooter)
        self.log.append((shooter.name, target.name, isHit))
        if isHit:
            self.die(target)
    def die(self, player):
        self.alivers.remove(player)
        
class Battle:
    def __init__(self, game):
        self.game = game
        self.rounds = []
    def run(self):
        alivers = self.game.players
        for time in range(100):
            if len(alivers) == 1:
                return alivers[0].name
            round = self.newRound(alivers)
            round.run()
            alivers = round.alivers
        raise Exception('dead loop')
    def newRound(self, alivers):
        round = BattleRound(alivers, self.game)
        self.rounds.append(round)
        return round


class GameRecord:
    def __init__(self, game):
        self.game = game
        self.times = 0
        self.wins = dict.fromkeys(map(lambda p: p.name, game.players), 0)
    def record(self, player):
        self.times += 1
        self.wins[player] += 1
    def playersInfo(self):
        playerStr = map(lambda p: '{}命中率{:.0%}'.format(p.name, p.rate/100), self.game.players)
        return '，'.join(playerStr)
    def gameInfo(self):
        gameStr = map(lambda p: '{}胜{}次，胜率{:.1%}'.format(p.name, self.wins[p.name], self.wins[p.name]/self.times), self.game.players)
        return '对决{}次。'.format(self.times) + '；'.join(gameStr) + "。"
    def __str__(self):
        return self.playersInfo() + '\n' + self.gameInfo()

class ShootRunner:
    def __init__(self, game):
        self.game = game
    def run_battle(self):
        return Battle(self.game).run()
    def run(self, times):
        record = GameRecord(self.game)
        for i in range(times):
            record.record(self.run_battle())
        return record.__str__()

def main():
    game = Game([('刘备', 30), ('曹操', 50), ('吕布', 100)])
    runner = ShootRunner(game)
    print(runner.run(10000))

if __name__ == '__main__':
    main()
