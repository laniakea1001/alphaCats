import PolicyValueNet
import Board
import Game
import MCTSPLayer
import PolicyValueNet

class Human(object):
    def __init__(self):
        self.player=None

    def set_player_ind(self,player):
        self.player=player

    def get_action(self,board):
        try:
            location=input("Your move:")
            if isinstance(location,str):
                location=[int(n,10) for n in location.split(",")]
                move=board.location_to_move(location)
        except Exception as e:
            move=-1

        if move==-1 or move not in board.availiable:
            print("invalid mive!!!")
            move=board.self.get_action(board)

        return move

    def __str__(self):
        return "HUman {}".format(self.player)

def run():
    n=5
    width,height=8,8
    model_file='current_policy.model'
    try:
        board=Board(width=width,height=height,n_in_row=n)
        game=Game(board)

        #create AI player
        best_policy=PolicyValueNet(width,height,model_file)
        mcts_playre=MCTSPLayer(best_policy.policy_value_fn,c_puct=5,n_playout=400)

        #create Human player
        human=Human()

        game.start_play(human,mcts_playre,start_player=1,is_show=1)
    except KeyboardInterrupt:
        print('\r\n quit!')


if __name__=="__main__":
        run()