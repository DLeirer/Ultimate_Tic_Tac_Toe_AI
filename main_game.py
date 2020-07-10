

######################################################
################## Global Variable   #################
######################################################


player = 2
enemy = 1
turn = 0
time_limit = 1
game_ultimate = Game(np.array([[4,4]]))
MC =MonteCarlo()



######################################################
################## game loop   #######################
######################################################

while True:
    turn += 1
    start_time = time.perf_counter()
    opponent_row, opponent_col = [int(i) for i in input().split()]
    valid_action_count = int(input())

    list_of_actions = []
    for i in range(valid_action_count):
        row, col = [int(j) for j in input().split()]
        list_of_actions.append([row, col])
    
    list_of_actions = np.asarray(list_of_actions)
    
    

    if opponent_row == -1:
        player = 1
        enemy = 2
    else:        
        game_ultimate.play_move(opponent_row,opponent_col)

    #print(["game_ultimate.game_board_full =",game_ultimate.game_board_full], file=sys.stderr, flush=True)   
    
    #MC = MonteCarlo()
    MC.reset_board(game_ultimate)

    n_loop=0
    current_time = time.perf_counter()
    elapsed_time = current_time - start_time
    while elapsed_time < time_limit:
        n_loop+=1
        
        MC.run_simulation(2)
        MC.reset_board(game_ultimate)
        
        current_time = time.perf_counter()
        elapsed_time = current_time - start_time

      
    time_limit = 0.0999
    print(["n loops =",n_loop], file=sys.stderr, flush=True)    
    if n_loop > 0:
        best_move,best_id_score = MC.best_move(player,enemy,list_of_actions)
        print(["best_move =",best_move], file=sys.stderr, flush=True) 
        print(["best_id_score =",best_id_score], file=sys.stderr, flush=True)       
    else:
        if [4,4] in list_of_actions.tolist():
            best_move = [4,4]
        else:
            best_move = list_of_actions[0]


    game_ultimate.play_move(best_move[0],best_move[1])
    

    print(str(best_move[0]) + " " + str(best_move[1]))
