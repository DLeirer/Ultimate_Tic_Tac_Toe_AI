import sys
import numpy as np
import math
import random
import time

        
class MonteCarlo():
    def __init__(self):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        #current state of game.
        self.states_dictionary = {}



    def update(self, visited_states,winner):
        final_score = np.sum(self.game_sim.game_board_top == -1)
        
        #np.sum(game_ultimate.game_board_top == -1)
        for state in visited_states:
          self.states_dictionary[state][0] += 1
          if winner == 1:
              self.states_dictionary[state][1] += 1
              final_score = np.sum(self.game_sim.game_board_top == 1) - np.sum(self.game_sim.game_board_top == -1)

              self.states_dictionary[state][3] += final_score

          elif winner == 2:
              self.states_dictionary[state][2] += 1
              final_score = np.sum(self.game_sim.game_board_top == -1) - np.sum(self.game_sim.game_board_top == 1)
              self.states_dictionary[state][3] += final_score

    def reset_board(self,board):
        self.game_sim = Game(board.legal_moves.copy())
        self.game_sim.game_board_top = board.game_board_top.copy()
        self.game_sim.game_board_full = board.game_board_full.copy()

    def best_move(self,player,enemy,legal_moves):
        #get child nodes. 
        possible_moves = self.game_sim.legal_moves
        child_node_ids = []
        #diction
        best_id = False
        best_id_score = -100000000
        #best_move = legal_moves[0]
        for move in possible_moves:
          #update state id
          child_node_id = self.game_sim.get_next_state_id(move[0],move[1])
          #self.game_sim.state_id+"_"+str(move[0])+str(move[1])
          #print(["child_node_id :",child_node_id], file=sys.stderr, flush=True)    
          if child_node_id in self.states_dictionary:              
             score = self.states_dictionary[child_node_id][player] / self.states_dictionary[child_node_id][0]
             score -= (self.states_dictionary[child_node_id][enemy] / self.states_dictionary[child_node_id][0]) * 1000
             score += (self.states_dictionary[child_node_id][3] / self.states_dictionary[child_node_id][0]) 
             if score > best_id_score:
                best_id_score = score
                best_id = child_node_id
                best_move = move.copy()
        
          
        
        return best_move, best_id_score

    def run_simulation(self,simulation_steps):
        # Plays out a "random" game from the current position,
        #while loop for the game. 
        visited_states = set()
        n=0
        #print("n =",n )


        while self.game_sim.game_over == False:
          leaf_found = False
          #choose random move. 
          possible_moves = self.game_sim.legal_moves
          for pos_move in possible_moves:
              next_state_id = self.game_sim.get_next_state_id(pos_move[0],pos_move[1])
              if next_state_id not in self.states_dictionary:
                  self.game_sim.play_move(pos_move[0],pos_move[1])
                  self.states_dictionary[next_state_id] = [1,1,1,1]
                  #visited_states.add(next_state_id)
                  leaf_found = True
                  #print(["break 1"], file=sys.stderr, flush=True)   
                  break
          
          if leaf_found == False:
              #best node
              if self.game_sim.current_player == 1:
                  move,id=self.best_move(1,2,possible_moves)
              else:
                  move,id=self.best_move(2,1,possible_moves)

              self.game_sim.play_move(move[0],move[1])

          #n_int = random.randint(0,len(possible_moves)-1)
          #print("n int",n_int)
          #move = possible_moves[n_int]
          #print("Move =",move)
          #play move
          #self.game_sim.play_move(move[0],move[1])
          

          #check if new state is in dictionary. if not add. 
          #if self.game_sim.state_id not in self.states_dictionary:
          #    self.states_dictionary[self.game_sim.state_id] = [0,0,0,0] #0 = visits, 1 player 1 wins, 2, player 2 wins, 3, draw.

          #add state_id to visited states.
          visited_states.add(self.game_sim.state_id)
          n+=1
          #print(["n1"], file=sys.stderr, flush=True) 
          #print("n = ",n)
          if n > simulation_steps:
            #print(["break 2"], file=sys.stderr, flush=True) 
            break
        

        #update states dictionary
        self.update(visited_states,self.game_sim.winner)
