# -*- coding: utf-8 -*-
import PieceModels as pm
import PlayerModel as pp
import util as u
class Heap:

    def __init__(self):
        self.heap_list = pm.GroupPieces()

    def getHeap(self):
        return self.heap_list

    def setHeap(self, pieces):
        self.heap_list = pieces

    def shuffleHeap(self):
        self.heap_list.shuffle()

    def len(self):
        return self.heap_list.lenGroupPieces()


class HandSupport:

    def __init__(self):
        self.piece_list = pm.GroupPieces()

    def setHand(self, pieces):
        self.piece_list = pieces

    def getHand(self):
        return self.piece_list

    def pop(self, p):
        return self.piece_list.popPiece(p)

    def len(self):
        return self.piece_list.lenGroupPieces()

    def sumValue(self):
        return self.piece_list.getSumValue()

    def maxValue(self):
        return self.piece_list.getMaxValue()

