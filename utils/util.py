

def parseArguments(sys_ref):
    len_args = len(sys_ref.argv)
    if(len_args <= 5):
        print('Parameters missing...')
        print('\t-p "Player_1" "Player_2"')
        print('\t-s "Game Score"')
        print('\n\nexiting...')
        sys_ref.exit()
    for i in range(1, len_args):
        if(sys_ref.argv[i] == '-p')
            player_list = list()
            for j in range(i + 1, len_args):
                if(sys_ref.argv[j][0] == '-')
                    break
                player_list.append(Player(sys_ref.argv[j]))
        if(sys_ref.argv[i] == '-s'):
            score = sys_ref.argv[i + 1]
    return player_list, score

