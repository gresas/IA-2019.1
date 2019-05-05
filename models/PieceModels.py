import random
from .utils import util as u

class Piece:
    def __init__(self, left, right):
        self.left_value = left
        self.right_value = right  
        self.value = left + right

    def isFoldedPiece(self):
        return (self.left_value == self.right_value)

    def isCorrect(self, table_pieces):
        if(not table_pieces):
            return True
        first_left, last_right = u.parseGameTable(table_pieces)
        if((self.left_value == first_left) or (self.right_value == first_left) \
        or (self.left_value == last_right) or (self.right_value == last_right)):
            return True                
        return False    

    def getString(self):
        return '|%s|%s|'%(self.left_value, self.right_value)

    def printPiece(self):
        print('|%s|%s| '%(self.left_value, self.right_value))
        

class GroupPieces:
    def __init__(self):
        self.pieces = list()

    def getPosition(self, peca):
        return self.pieces.index(peca)

    def getPieceFromIndex(self, position):
        return self.pieces[position]

    def getSumValue(self):
        return sum(list(map(lambda x: x.value, self.pieces)))

    def getGroupPieces(self):
        return self.pieces

    def getMaxValue(self):
        return max([p.totalValue() for p in self.pieces])

    def appendPiece(self, p):
        self.pieces.append(p)

    def popPiece(self, p):
        return self.pieces.pop(self.getPosition(p))

    def popIndexPiece(self, pos):
        return self.pieces.pop(pos)

    def lenGroupPieces(self):
        return len(self.pieces)

    def randomChoose(self):
        random.seed()
        return random.choice(self.pieces)

    def shuffle(self):
        random.shuffle(self.pieces)

    def printPieces(self):
        print_obj = [p.getString() for p in self.pieces]
        print(" : ".join(print_obj))
        
        #u.fancyPrintPiece(p, (p == self.pieces[len(self.pieces)-1]))
    def followTheRules(self, table_pieces):
        if(not table_pieces):
            return True
        first_left, last_right = u.parseGameTable(table_pieces)
        # print('\n',(first_left, last_right))
        for this_p in self.pieces:
            #this_p.printPiece()
            if((this_p.left_value == first_left) or (this_p.right_value == first_left) \
            or (this_p.left_value == last_right) or (this_p.right_value == last_right)):
                return True
        return False

    def clear(self):
        self.pieces.clear()
