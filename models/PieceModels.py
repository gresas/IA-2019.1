import random

class Piece:
    def __init__(self, left, right):
        self.left_value = left
        self.right_value = right  

    def totalValue(self):
        return self.left_value + self.right_value


class GroupPieces:
    def __init__(self):
        self.pieces = list()

    def getPosition(self, peca):
        return self.pieces.index(peca)

    def getPieceFromIndex(self, position):
        return self.pieces[position]

    def getGroupPieces(self):
        return self.pieces

    def appendPiece(self, p):
        self.pieces.append(p)

    def popPiece(self, p):
        return self.pieces.pop(self.getPosition(p))

    def lenGroupPieces(self):
        return len(self.pieces)

    def randomChoose(self):
        random.seed()
        return random.choice(self.pieces)

    def shuffle(self):
        random.shuffle(self.pieces)

    def getSumValue(self):
        return sum(list(map(lambda x: x.value, self.pieces)))

    def clear(self):
        self.pieces.clear()
