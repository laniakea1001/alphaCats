import numpy as np

import Board

class Game(object):

    def __init__(self,board:Board):
        self.board=board

    def starrt_self_play(self,player,is_show=False,temp=1e-3):
        self.board.init_board()
        p1,p2=self.board.players
        states,mcts_probs,current_players=[],[],[]
        while(1):
            move,move_probs=player.get_action(self.board,temp=temp,return_prob=1)

            #save data of self-play
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append((self.board.current_player))
            #run a step
            self.board.do_move(move)
            if is_show:
                self.graphic(self.board,p1,p1)
            end,winner=self.board.game_over()
            if end:
                #save win data form ervey view of player
                winners_z=np.zeros(len(current_players))
                if winner !=-1:
                    winners_z[np.array(current_players)==winner]=1.0
                    winners_z[np.array(current_players)!=winner]=-1.0

                player.reset_player()
                if is_show:
                    if winner!=-1:
                        print("Game end.Winner is player:",winner)
                    else:
                        print("Game end.Tie")
                return winner,zip(states,mcts_probs,winners_z)

    def start_play(self,player1,player2,start_player=0,is_show=1):
        if start_player not in (0,1):
            raise Exception('start_player should be either 0 or 1')

        self.board.init_board(start_player=start_player)
        p1,p2=self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players={p1:player1,p2:player2}

        if is_show:
            self.graphic(self.board,player1,player2,players.player)
        while (1):
            current_player=self.board.get_curent_player()
            player_in_turn=players[current_player]
            move=player_in_turn.get_Action(self.board)
            self.board.do_move(move)
            if is_show:
                self.graphic(self.board,player1.player,player2.player)
                end,winner=self.board.game_over()
            if end:
                if is_show:
                    if winner !=-1:
                        print("Game end.Winner is",players[winner])
                    else:
                        print("Game end.Tie")

                return winner

    def graphic(self,board,player1,player2):
        width=board.width
        height=board.height

        print("Player",player1,"Width X".rjust(3))
        print("Player",player2,"width O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x),end='')

        print('\r\n')
        for i in range(height-1,-1,-1):
            print("{0:4d}".format(i),end='')
            for j in range(width):
                loc=i*width+j
                p=board.states.get(loc,-1)
                if p == player1:
                    print('X'.center(8),end='')
                elif p==player2:
                    print('O'.center(8),end='')
                else:
                    print('_'.center(8),end='')
            print('\r\n\r\n')

