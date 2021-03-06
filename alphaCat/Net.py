import numpy as np
import tensorflow
import torch.nn as nn
import torch.nn.functional as F

def set_laerning_rate(optimizer,lr):
    for param_group in optimizer.param_group:
        param_group['lr']=lr


class Net():
    def __init__(self,board_width,board_height):
        super(Net,self).__init__()
        self.board_width=board_width
        self.board_height=board_height

        self.conv1=nn.Conv2d(4,32,kernel_size=3,padding=1)
        self.conv2=nn.Conv2d(32,64,kernel_size=3,padding=1)
        self.conv3=nn.Conv2d(64,128,kernel_size=3,padding=1)

        #action policy layers
        self.act_conv1=nn.Conv2d(128,2,kernel_size=1)
        self.act_fc1=nn.Linear(4*board_height*board_width,board_height*board_width)

        #state value layers
        self.val_conv1=nn.Conv2d(128,2,kernel_size=1)
        self.val_fc1=nn.Linear(2*board_width*board_height,64)
        self.val_fc2=nn.Linear(64.1)


    def forward(self,state_input):
        x=F.relu(self.conv1(state_input))
        x=F.relu(self.conv2(x))
        x=F.relu(self.conv3(x))

        x_act=F.relu(self.act_conv1(x))
        x_act=x_act.view(-1,4*self.board_width*self.board_height)
        x_act=F.log_Softmax(self.act_fc1(x_act))

        x_val=F.relu(self.val_conv1(x))
        x_val=x_val.view(-1,2*self.board_width*self.board_height)

        x_val=F.relu(self.val_fc1(x_val))
        x_val=F.tanh(self.val_fc2(x_val))
        return x_act,x_val







