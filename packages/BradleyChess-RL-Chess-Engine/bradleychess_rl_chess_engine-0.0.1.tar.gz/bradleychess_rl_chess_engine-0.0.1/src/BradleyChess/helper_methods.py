import Bradley as imman
import pandas as pd

def init_bradley(chess_data):
    """ the object needs to be instantiated with some chess data, 
        even if the agents have already been trained.
    """
    bubs = imman.Bradley(chess_data)
    return bubs


def play_game(bubs, rl_agent_color):
    """ use this method to play against a human player 
    """
    W_turn = True
    turn_num = bubs.get_curr_turn()

    if rl_agent_color == 'W':
        rl_agent = bubs.W_rl_agent
    else:
        rl_agent = bubs.B_rl_agent
    
    while bubs.game_on():
        if W_turn:
            player_turn = 'W'
        else:
            player_turn = 'B'
        
        print(f'\nCurrent turn is :  {turn_num}')
        
        if rl_agent.color == player_turn:
            print('=== RL AGENT\'S TURN ===')
            chess_move = bubs.rl_agent_chess_move(rl_agent.color)
            chess_move_str = chess_move['chess_move_str']
            print(f'RL agent played {chess_move_str}\n')
        else:
            print('=== OPPONENT\' TURN ===')
            chess_move = str(input('hooman, enter chess move: '))
            print('\n')
            
            while not bubs.recv_opp_move(chess_move):  # this method returns False for incorrect input
                print('invalid input, try again')
                chess_move = str(input('enter chess move: '))
        
        turn_num = bubs.get_curr_turn()
        W_turn = not W_turn # simple flag to switch the turn to B or vice-versa
    
    print(f'Game is over, result is: {bubs.get_game_outcome()}')
    print(f'The game ended because of: {bubs.get_game_termination_reason()}')
    bubs.reset_environ()


def agent_vs_agent(bubs):
    """ play two trained agents against each other """
    W_turn = True
    turn_num = bubs.get_curr_turn()
    
    while bubs.game_on():        
        # bubs's turn
        print(f'\nCurrent turn: {turn_num}')
        chess_move_bubs = bubs.rl_agent_chess_move('W')
        bubs_chess_move_str = chess_move_bubs['chess_move_str']
        print(f'Bubs played {bubs_chess_move_str}\n')

        # imman's turn, check for end of game again, since the game could have ended after W's move.
        if bubs.game_on():
            turn_num = bubs.get_curr_turn()
            print(f'Current turn:  {turn_num}')
            chess_move_imman = bubs.rl_agent_chess_move('B')
            imman_chess_move_str = chess_move_imman['chess_move_str']
            print(f'Imman played {imman_chess_move_str}\n')

        print(bubs.environ.board)
        
        turn_num = bubs.get_curr_turn()
        W_turn = not W_turn
    
    print('Game is over, chessboard looks like this:\n')
    print(bubs.environ.board)
    print('\n\n')
    print(f'Game result is: {bubs.get_game_outcome()}')
    print(f'Game ended because of: {bubs.get_game_termination_reason()}')
    bubs.reset_environ()


def pikl_q_table(bubs, rl_agent_color, q_table_path):
    """ make sure to get input the correct q_table_path for each agent """
    if rl_agent_color == 'W':
        rl_agent = bubs.W_rl_agent
    else:
        rl_agent = bubs.B_rl_agent

    rl_agent.Q_table.to_pickle(q_table_path, compression = 'zip')


def bootstrap_agent(bubs, rl_agent_color, existing_q_table_path):
    """ assigns an agents q table to an existing q table.
        make sure the q table you pass matches the color of the agent.
        Use this method when retraining an agent or when you want agents
        to play against a human or each other.

        It's very important to pass in the correct q table path
    """
    if rl_agent_color == 'W':
        rl_agent = bubs.W_rl_agent
    else:
        rl_agent = bubs.B_rl_agent

    rl_agent.Q_table = pd.read_pickle(existing_q_table_path, compression = 'zip')
    rl_agent.is_trained = True