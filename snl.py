import json
import random
from copy import deepcopy

class Board:

    def __init__(self, name):
        with open('boards.json') as f:
            data = json.load(f)[name]
        self.size = data['size']
        self.graph = {int(x): y for x, y in data['graph'].items()}

    def validate(self):
        for k,v in self.graph.items():
            if int(k)>self.size or int(v)>self.size:
                #print('Invalid snake or ladder. Vector points off board')
                return False
        keys = [int(x) for x in self.graph.keys()]
        vals = [int(x) for x in self.graph.values()]
        if len(set(vals))!=len(vals):
            #print('Invalid snake or ladder. Multiple vectors point to common spot.')
            return False
        if len(set(keys)&set(vals))>0:
            #print('Invalid snake or ladder. Chained vectors.')
            #print(set(keys)&set(vals))
            return False
        return True

    def get_perturbs(self,dx=1):
        for k,v in self.graph.items():
            for x in [-dx,dx]:
                temp = deepcopy(self)
                del temp.graph[k]
                temp.graph[k+x] = v
                if temp.validate():
                    yield temp
                temp = deepcopy(self)
                temp.graph[k] = v+x
                if temp.validate():
                    yield temp

class Player:
    def __init__(self):
        self.place = 0
        self.history = [0]

    def roll(self):
        return random.randint(1, 6)

    def move(self, board):
        n = self.roll()
        place = self.place + n
        if place in board.graph:
            place = board.graph[place]
        self.place = place
        self.history.append(self.place)

    def reset(self):
        self.place = 0
        self.history = [0]

    def validate(self):
        # Maybe put a validation here
        return True


class Game:
    def __init__(self, board=None, player=None):
        if player is None:
            self.player = Player()
        if board is None:
            self.board = Board('default')
        elif type(board) == str:
            self.board = Board(board)
        else:
            self.board = board
        self.log = []

    def play(self, n=1):
        for i in range(n):
            self.player.reset()
            while self.player.place < self.board.size:
                self.player.move(self.board)
            self.log.append(self.player.history)

    def reset(self):
        self.log = []

    def validate(self):
        return self.board.validate() and self.player.validate()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    game = Game()
    N=5
    bigavgs = []
    for i in range(N):
        avgs = []
        for b in game.board.get_perturbs():
            if not b.validate():
                continue
            g = Game(b)
            print('Playing games..')
            g.play(10000)
            lens = [len(x) for x in g.log]
            a = sum(lens)/len(lens)
            print('Avg game length:',a)
            avgs.append(a)
            #print('Plotting results..')
            #plt.hist(lens, bins=range(max(lens)+1))
    bigavgs.append(avgs)
    bigavgs = np.array(bigavgs).mean(axis=0)
    print(bigavgs)
    plt.plot(bigavgs)
    plt.show()
