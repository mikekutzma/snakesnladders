import json
import random

class Board:
    # TODO: Add board validation
    def __init__(self, name):
        with open('boards.json') as f:
            data = json.load(f)[name]
        self.size = data['size']
        self.graph = {int(x): y for x, y in data['graph'].items()}


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


if __name__ == "__main__":
    game = Game()
    print('Playing games..')
    game.play(10000)
    lens = [len(x) for x in game.log]
    print('Plotting results..')
    maxlen = 150
    lens = [x for x in lens if x < maxlen]
    plt.hist(lens, bins=list(range(maxlen)))
    plt.show()
