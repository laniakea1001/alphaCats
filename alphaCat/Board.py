import numpy as np


class Board(object):
    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 8))
        self.height = int(kwargs.get('height', 8))
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.players = (1, 2)
        self.states = {}

    def init_board(self, start_player=0):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not be less then {}'.format(self.n_in_row))
        # The No of current player
        self.current_player = self.players[start_player]
        self.availiable = list(range(self.width * self.height))
        self.states = {}
        self.last_move = -1

    def move_to_location(self,move):
        """
        3*3 boards moves like:
          6 7 8
          3 4 5
          0 1 2
          and move 5's location is (1,2)
        """
        h=move//self.width
        w=move%self.width
        return [h,w]

    def location_to_move(self,location):
        if len(location)!=2:
            return -1
        h=location[0]
        w=location[1]
        move=h*self.width+w
        if move not in range(self.width*self.height):
            return -1
        return move

    def do_move(self,move):
        self.states[move]=self.current_player
        self.availiable.remove(move)
        self.current_player=(self.players[0] if self.current_player==self.players[1] else self.players[1])
        self.last_move=move

    def get_curent_player(self):
        return self.current_player

    def current_state(self):
        square_state=np.zeros((4,self.width,self.height))
        if self.states:
            moves,players=np.array(list(zip(*self.states.items())))
            move_curr=moves[players==self.current_player]
            move_oppo=moves[players!=self.current_player]
            square_state[0][move_curr//self.width,move_curr%self.height]=1.0
            square_state[1][move_oppo//self.width,move_oppo%self.height]=1.0
            square_state[2][self.last_move//self.width,self.last_move%self.height]=1.0

        if len(self.states)%2==0:
            square_state[3][:,:]=1.0
        return square_state[:,::-1,:]

    def has_a_winner(self):
        width=self.width
        height=self.height
        states=self.states
        n=self.n_in_row

        moved=list(set(range(width*height))-set(self.availiable))
        if(len(moved)<self.n_in_row+2):
            return False,-1

        for m in moved:
            h=m//width
            w=h%width
            player=states[m]

            if(w in range(width-n+1) and len((set(states.get(i,-1) for i in range(m,m+n)))==1)):
                return True,player

            if(h in range(height-n+1)and len(set(states.get(i,-1)for i in range(m,m+n*width,width)))==1):
                return True,player

            if (w in range(width-n+1)and h in range(height-n+1)and len(set(states.get(i,-1) for i in range(m,m+n*(width+1),width+1)))==1):
                return True,player

            if(w in range(n-1,width)and h in range(height-n+1)and len(set(states.get(i,-1)for i in range(m,m+n*(width-1),width-1)))==1):
                return False,-1

    def game_over(self):
        win,winner=self.has_a_winner()
        if win:
            return True,winner
        elif not len(self.availiable):
            return True,-1
        return False,-1
