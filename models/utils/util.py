from .. import PlayerModel as pm

def parseArguments(sys_ref):
    len_args = len(sys_ref.argv)
    if(len_args <= 5):
        print('Parameters missing...')
        print('\t-p "Player_1" "Player_2"')
        print('\t-s "Game Score"')
        print('\n\nexiting...')
        sys_ref.exit()
    for i in range(1, len_args):
        if(sys_ref.argv[i] == '-p'):
            player_list = list()
            for j in range(i + 1, len_args):
                if(sys_ref.argv[j][0] == '-'):
                    break
                player_list.append(pm.Player(sys_ref.argv[j]))
        if(sys_ref.argv[i] == '-s'):
            score = sys_ref.argv[i + 1]
    return (player_list, score)

def turnMenu(player):
    print('Player of the turn: %s'%player.nick)
    print('Here is your hand: \n')
    player.printHand()
    opt = int(input("\nEntre com a posicao da peca a ser jogada:\n"))
    return opt

def isTieGame(tuple_list):
    value = tuple_list[0]
    for t in tuple_list:
        if(t[0] != value):
            return False
    return True

def parseGameTable(table_tuple):
    if(table_tuple):
        return table_tuple[0][0], table_tuple[-1][1]
