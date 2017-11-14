from argparse import ArgumentParser
from random import randint

class SelectHighestRateStrategy:
    def chooseTarget(self, opponents):           
        opponents = sorted(opponents, key=lambda p:p.rate)
        return opponents[-1]
    def __str__(self):
        return '射击命中率最高对手'
class WaitForOneOpponentStrategy:
    def chooseTarget(self, opponents):           
        return None if len(opponents) != 1 else opponents[0] 
    def __str__(self):
        return '等待剩下一名对手再射击'

class Player:
    def __init__(self, name, rate, strategy=SelectHighestRateStrategy()):
        self.name = name
        self.rate = rate
        self.strategy = strategy
    def chooseTarget(self, alivers):           
        opponents = list(alivers)
        opponents.remove(self)
        return self.strategy.chooseTarget(opponents)
    def isHit(self):
        return randint(1,100) <= self.rate
    def __str__(self):
        return '{}命中率{:.0%}，{}'.format(self.name, self.rate/100, self.strategy)
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class BattleRound:
    def __init__(self, players):
        self.log = []
        self.alivers = list(players)
    def run(self):
        for player in self.alivers:
            if len(self.alivers) == 1: return
            self.shoot(player)
    def shoot(self, shooter):
        target = shooter.chooseTarget(self.alivers)
        if target is None:
            self.log.append((shooter.name, None, False))
        else:
            isHit = shooter.isHit()
            self.log.append((shooter.name, target.name, isHit))
            if isHit: self.die(target)
    def die(self, player):
        self.alivers.remove(player)
        
class Battle:
    def __init__(self, players):
        self.players = players
        self.rounds = []
        self.winner = None
    def run(self):
        alivers = self.players
        for time in range(100):
            if len(alivers) == 1:
                self.winner = alivers[0].name
                return self
            round = self.newRound(alivers)
            round.run()
            alivers = round.alivers
        raise Exception('dead loop')
    def newRound(self, alivers):
        round = BattleRound(alivers)
        self.rounds.append(round)
        return round
    def __str__(self):
        str = '=========='
        for i in range(len(self.rounds)):
            str += '\n第{}轮：'.format(i+1)
            for shoot in self.rounds[i].log:
                str += '\n' + self.formatShootInfo(*shoot)
        str += '\n对决结束：{}胜。'.format(self.winner)
        return str
    def formatShootInfo(self, shooter, target, isHit):
        templet = '{0}朝天射击。' if target is None else '{0}射击{1}，命中。{1}死。' if isHit else '{}射击{}，未命中。'
        return templet.format(shooter,target)


class GameRecord:
    def __init__(self, players):
        self.players = players
        self.times = 0
        self.wins = dict.fromkeys(map(lambda p: p.name, players), 0)
        self.details = []
    def record(self, battle):
        self.times += 1
        self.wins[battle.winner] += 1
        self.details.append(battle)
    def playersInfo(self):
        playerStr = map(Player.__str__, self.players)
        return '。'.join(playerStr) + '。'
    def gameInfo(self):
        gameStr = map(lambda p: '{}胜{}次，胜率{:.1%}'.format(p.name, self.wins[p.name], self.wins[p.name]/self.times), self.players)
        return '对决{}次。\n'.format(self.times) + '；\n'.join(gameStr) + "。"
    def __str__(self):
        return '--------------------\n' + self.playersInfo() + '\n' + self.gameInfo()

class ShootRunner:
    def __init__(self, playerTuples):
        self.players = list(map(lambda p: Player(*p), playerTuples))
    def run_battle(self):
        return Battle(self.players).run()
    def run(self, times):
        record = GameRecord(self.players)
        for i in range(times):
            record.record(self.run_battle())
        return record

showDetials = False
def main():
    printGame( ShootRunner([('刘备', 10), ('曹操', 20), ('吕布', 100)]) )
    printGame( ShootRunner([('刘备', 10, WaitForOneOpponentStrategy()), ('曹操', 20), ('吕布', 100)]) )

def printGame(runner):
    record = runner.run(10000)
    print( record.__str__() )
    if showDetials:
        print( record.details[365].__str__() + '\n......\n' )


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-v', help='print game details', action='store_true')
    args = parser.parse_args()
    showDetials = args.v
    main()
