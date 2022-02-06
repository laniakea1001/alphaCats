import torch
import numpy as np
import Net
import Board
import torch.optim as optim
import torch.autograd as Variable
import torch.nn.functional as F

class PolicyValueNet():
    def __init__(self,board_width,board_height,model_file=None):
        self.board_width=board_width
        self.board_height=board_height
        self.l2_const=1e-4
        self.policy_value_net=Net(board_width,board_height)
        self.optimizer=optim.Adam(self.policy_value_net.parameters(),weight_decay=self.l2_const)
        if model_file:
            net_param=torch.load(model_file)
            self.policy_value_net.load_state_dict(net_param)


    def policy_value_fn(self,board:Board):
        legal_positions=board.availiable
        current_state=np.ascontiguousarray(board.current_state().reshape(-1,4,self.board_width,self.board_height))
        log_act_probs,value=self.policy_value_net(Variable(torch.from_numpy(current_state)).float())
        act_probs=np.exp(log_act_probs.data.numpy().flattern())
        act_probs=zip(legal_positions,act_probs[legal_positions])
        value=value.data[0][0]
        return act_probs,value


    def train_step(self,state_batch,mcts_probs,winner_batch,lr):
        state_batch=Variable(torch.FloatTensor(state_batch))
        mcts_probs=Variable(torch.FloatTensor(mcts_probs))
        winner_batch=Variable(torch.FloatTensor(winner_batch))
        self.optimizer.zero_grad()
        self.sel_learning_rate(self.optimizer,lr)

        log_act_ptobs,value=self.policy_value_net(state_batch)
        value_loss=F.mse_loss(value.view(-1),winner_batch)
        policy_loss=-torch.mean(torch.sum(mcts_probs*log_act_ptobs,1))
        loss=value_loss+policy_loss
        loss.backword()
        self.optimizer.step()
        entropy=-torch.mean(torch.sum(torch.exp(log_act_ptobs)*log_act_ptobs,1))

        return loss.data[0],entropy.data[0]

    def get_policy_param(self):
        net_param=self.policy_value_net.state_dict()
        return net_param

    def save_model(self,model_file):
        net_param=self.get_policy_param()
        torch.save(net_param,model_file)

    def sel_learning_rate(self,optimizer:torch.optim,lr):
        for param_group in optimizer.param_groups:
            param_group['lr']=lr
