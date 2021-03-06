from tkinter import *
import copy

""" The GUI for the game, along with any interactions with it.

Note: Currently player 1 is always nought, and player 2 / CPU is always cross.
"""
class NoughtsAndCrossesScreen:
    def __init__(self):
        """ Creates the screen and the initial grid & player states.

        There are two game modes available: PvP or PvCPU. To switch
        between the two, change the "self.CPU_opponent_enabled" flag.
        """
        self.width = 600
        self.height = 600
        self.cell_width = self.width // 3
        self.cell_height = self.height // 3
        self.grid_state = [[None, None, None],
                           [None, None, None],
                           [None, None, None],]
        
        self.CPU_opponent_enabled = True
        if self.CPU_opponent_enabled:
            self.CPU_opponent = NoughtsAndCrossesMinimaxAI()
            self.current_player = "Player"
        else:
            self.current_player = "Player 1"
        
        self.root = Tk()
        self.root.geometry = str(self.width) + "x" + str(self.height)
        self.root.resizable(width = False, height = False)
        self.root.title = "Noughts and Crosses"
        self.create_grid()
        self.root.mainloop()

    def create_grid(self):
        """Create the noughts and crosses grid.

        Create a Canvas, draw grid lines, bind the canvas to respond to
        a button press.
        """
        self.grid = Canvas(self.root, width = self.width, height = self.height)
        self.grid.pack()
        for i in range(1,3):
            self.grid.create_line(self.cell_width * i, 0,
                                  self.cell_width * i, self.height)
            self.grid.create_line(0, self.cell_height * i,
                                  self.width, self.cell_height * i)
        self.grid.bind("<Button-1>", self.perform_action)

    def check_win_or_tie(self):
        """ Return the winning player, no current winner or a tie.

        First identify which player is playing - we use this to
        identify which symbol to check. Then check the grid state
        for a 3-in-a-row of the player's symbol. If there is then
        a player has won, if not then play resumes unless the grid
        is full (in which case it is a tie).
        Note that this function is run after a player makes an action,
        before the player turn is switched.

        Return
        ------------
            winner: string
                Which player won, if any.
        """
        
        if self.current_player == "Player 1" or self.current_player == "Player":
            symbol = "nought"
        else:
            symbol = "cross"

        for row_num in range(3):
            if self.grid_state[row_num] == [symbol, symbol, symbol]:
                return self.current_player
        for col_num in range(3):
            if (self.grid_state[0][col_num] == symbol
                and self.grid_state[1][col_num] == symbol
                and self.grid_state[2][col_num] == symbol):
                # If all are True then a vertical 3-in-a-row was found
                return self.current_player
        if self.grid_state[1][1] == symbol:
            if ((self.grid_state[0][0] == symbol
                 and self.grid_state[2][2] == symbol) or
                (self.grid_state[0][2] == symbol
                 and self.grid_state[2][0] == symbol)):
                # Checks for either diagonal match
                return self.current_player   

        full_board = True
        for row in range(3):
            for col in range(3):
                if self.grid_state[row][col] is None:
                    full_board = False
        if full_board:
            return "Tie"

        # If no return has been made by this point, it is assumed that
        # no one has won nor is it a tie.
        return None

        
    def add_nought(self, placements):
        """ Add a nought symbol onto the grid and the 2D array.

        Draws a nought symbol on the grid in the specified row and column,
        and modifies the 2D array to reflect the new board state.

        Parameters
        ------------
            placements: (int, int)
                The (row, column) the symbol will be placed in.
        """
        row, column = placements
        centerpoint_x = self.cell_width / 2 + (self.cell_width * column)
        centerpoint_y = self.cell_height / 2 + (self.cell_height * row)
        self.grid.create_oval(centerpoint_x - 67, centerpoint_y - 67,
                              centerpoint_x + 67, centerpoint_y + 67)
        self.grid_state[row][column] = "nought"

    def add_cross(self, placements):
        """ Add a cross symbol onto the grid and the 2D array.

        Draws a cross symbol on the grid in the specified row and column,
        and modifies the 2D array to reflect the new board state.

        Parameters
        ------------
            placements: (int, int)
                The (row, column) the symbol will be placed in.
        """
        row, column = placements
        centerpoint_x = self.cell_width / 2 + (self.cell_width * column)
        centerpoint_y = self.cell_height / 2 + (self.cell_height * row)
        self.grid.create_line(centerpoint_x - 67, centerpoint_y - 67,
                              centerpoint_x + 67, centerpoint_y + 67)
        self.grid.create_line(centerpoint_x + 67, centerpoint_y - 67,
                              centerpoint_x - 67, centerpoint_y + 67)
        self.grid_state[row][column] = "cross"
            
    def display_tied_game_message(self):
        """ Displays a message stating the game is tied.

        Message is displayed through a pop-up box, and there is a button
        the user can click to restart the game. Closing the screen instead
        also restarts the game.
        """
        tied_popup = Tk()
        tied_popup.title(" ")
        tied_popup.protocol("WM_DELETE_WINDOW",
                            lambda:[tied_popup.destroy(), self.restart_game()])
        tied_message = Label(tied_popup, text = "It's a tie!")
        tied_message.place(relx = 0.5, rely = 0.2, anchor = N)
        restart_button = Button(tied_popup, text = "Restart",
                                command = lambda:[tied_popup.destroy(),
                                                  self.restart_game()])
        restart_button.place(relx = 0.5, rely = 0.8, anchor = S)
        tied_popup.mainloop()

    def display_win_message(self, winner):
        """ Displays a message notifying the user who won.

        Message is displayed through a pop-up box, and there is a button
        the user can click to restart the game. Closing the screen instead
        also restarts the game.

        Parameters
        ------------
            winner: string
                The player who won the game.
        """
        win_popup = Tk()
        win_popup.title(" ")
        win_popup.protocol("WM_DELETE_WINDOW",
                           lambda:[win_popup.destroy(), self.restart_game()])
        win_message = Label(win_popup,
                            text = (self.current_player + " wins!"))
        win_message.place(relx = 0.5, rely = 0.2, anchor = N)
        restart_button = Button(win_popup, text = "Restart",
                                command = lambda:[win_popup.destroy(),
                                                  self.restart_game()])
        restart_button.place(relx = 0.5, rely = 0.8, anchor = S)
        win_popup.mainloop()

    def restart_game(self):
        """ Resets the game back to it's original state.

        The grid state is reset and the grid drawing is recreated.
        """
        self.grid_state = [[None, None, None],
                           [None, None, None],
                           [None, None, None],]
        self.grid.destroy()
        if self.CPU_opponent_enabled:
            self.CPU_opponent = NoughtsAndCrossesMinimaxAI()
            self.current_player = "Player"
        else:
            self.current_player = "Player 1"
        self.create_grid()

    def perform_action(self, event):
        """ Add a symbol to the grid, then check if a player has won and
            display a message if so. If not, the current player is switched.

        A preliminary check is made to ensure the user clicked on an empty
        space. If not then nothing happens.
        The symbol added is deduced by which player is playing and the
        position is determined by where the player clicked. Checking if
        a player has won and displaying a win message are both done
        through function calls.

        Parameters
        ------------
            event: object
                Contains the x and y coordinate the user pressed on. 
        """
        
        col = event.x // self.cell_width
        row = event.y // self.cell_height
        if self.grid_state[row][col] is None:
            if self.current_player == "Player 1" or self.current_player == "Player":
                self.add_nought((row, col))
            else:
                self.add_cross((row, col))
                
            winner = self.check_win_or_tie()
            if winner is not None:
                if winner == "Tie":
                    self.display_tied_game_message()
                else:
                    self.display_win_message(winner)
            else:
                if self.CPU_opponent_enabled == True:
                    if self.current_player == "Player":
                        self.current_player = "CPU"
                        self.take_CPU_action()
                    else:
                        self.current_player = "Player"
                elif self.current_player == "Player 1":
                    self.current_player = "Player 2"
                else:
                    self.current_player = "Player 1"

    def take_CPU_action(self):
        """ Lets the AI take it's turn."""
        action = self.CPU_opponent.determine_best_action(self.grid_state)
        position_found = False
        for row in range(3):
            for col in range(3):
                if self.grid_state[row][col] != action[row][col]:
                    position = (row, col)
                    self.add_cross(position)
                    position_found = True
                    self.grid_state = action
                    
                    winner = self.check_win_or_tie()
                    if winner is not None:
                        if winner == "Tie":
                            self.display_tied_game_message()
                        else:
                            self.display_win_message(winner)
                    else:
                        self.current_player = "Player"
                    
        if not position_found:
            print("No CPU action error.")
        

        
""" A Minimax AI for the game Noughts and Crosses"""
class NoughtsAndCrossesMinimaxAI:
    def __init__(self):
        self.winner_scores = {
            "CPU" : 1,
            "Tie" : 0.5,
            "None" : 0,
            "Player" : -1
            }
        
    def check_win_or_tie(self, current_player, grid_state):
        """ A version of check-win_or_tie that inputs the current player
            and board state.

        First identify which player is playing - we use this to
        identify which symbol to check. Then check the grid state
        for a 3-in-a-row of the player's symbol. If there is then
        a player has won, if not then play resumes unless the grid
        is full (in which case it is a tie).
        Note that this function is run after a player makes an action,
        before the player turn is switched.

        Parameters
        ------------
            current_player: string
                The player who just did an action
            grid_state: A 3x3 2D array of strings
                The board state to evaluate.
        Return
        ------------
            winner: string
                Which player won, if any.
        """
        
        if current_player == "Player 1" or current_player == "Player":
            symbol = "nought"
        else:
            symbol = "cross"

        for row_num in range(3):
            if grid_state[row_num] == [symbol, symbol, symbol]:
                return current_player
        for col_num in range(3):
            if (grid_state[0][col_num] == symbol
                and grid_state[1][col_num] == symbol
                and grid_state[2][col_num] == symbol):
                # If all are True then a vertical 3-in-a-row was found
                return current_player
        if grid_state[1][1] == symbol:
            if ((grid_state[0][0] == symbol
                 and grid_state[2][2] == symbol) or
                (grid_state[0][2] == symbol
                 and grid_state[2][0] == symbol)):
                # Checks for either diagonal match
                return current_player   

        full_board = True
        for row in range(3):
            for col in range(3):
                if grid_state[row][col] is None:
                    full_board = False
        if full_board:
            return "Tie"

        # If no return has been made by this point, it is assumed that
        # no one has won nor is it a tie.
        return None

    def evaluate_state_score(self, to_evaluate, player_turn):
        """ Observes a game state to determine a score for the AI.

        A higher score is better for the AI.
        Points are awarded for states that make it more likely for the
        AI to win or tie, whereas points are deducted for states that
        make it more likely for the player to win.

        Parameters
        ------------
            to_evaluate: A 3x3 2D array of strings
                The game state to be evaluated
            player_turn: string
                The player who just took their turn. Used to decide
                whether to maximise or mimimse the score.

        Return
        ------------
            score: float
                The evaluated score for the game state.
        """
        winner = self.check_win_or_tie(player_turn, to_evaluate)
        if winner is not None:
            return self.winner_scores[winner]
        best_score = -2
        worst_score = 2
        if player_turn == "CPU":
            next_player = "Player"
        else:
            next_player = "CPU"
        next_player_actions = self.identify_possible_actions(next_player,
                                                             to_evaluate)
        for action in next_player_actions:
            score = self.evaluate_state_score(action, next_player)
            if next_player == "CPU":
                best_score = max(score, best_score)
            elif next_player == "Player":
                worst_score = min(score, worst_score)
            if best_score == 1:
                return best_score
            elif worst_score == -1:
                return worst_score
        if next_player == "CPU":
            return best_score
        return worst_score

    def identify_possible_actions(self, player, grid_state):
        """ Observes a game state and player turn to determine
            possible actions for that player.

        The "possible actions" includes actions that would cause the
        player to lose or win the game.

        Parameters
        ------------
            player: string
                The player who will be taking the next turn / action.
            grid_state: A 3x3 2D array of strings
                The game state to be evaluated.

        Return
        ------------
            possible_states: A list of 3x3 2D arrays of strings
                A list of possible game states from the inputted one. 
        """
        if player == "Player":
            symbol = "nought"
        else:
            symbol = "cross"
        possible_actions = []
        for row in range(3):
            for col in range(3):
                to_add = copy.deepcopy(grid_state)
                if grid_state[row][col] is None:
                    to_add[row][col] = symbol
                    possible_actions.append(to_add)
        return possible_actions

    def determine_best_action(self, grid_state):  
        """ Identifies the best action for the AI to take next.

        Uses a minimax algorithm to determine what the best action the
        AI should take.

        Parameters
        ------------
            current_game_state:
                The game state to evaluate and decide the best action from
        Return
        ------------
            best_action: A 3x3 2D array of strings
                The grid state following the best action taken.
        """
        possible_actions = self.identify_possible_actions("CPU",
                                                          grid_state)
        if len(possible_actions) < 1:
            print("grid state error")
        elif len(possible_actions) == 1:
            return possible_actions[0]
        else:
            best_action = []
            best_score = -2
            for action in possible_actions:
                score = self.evaluate_state_score(action, "CPU")
                if score == 1:
                    return action
                elif score > best_score:
                    best_action = action
                    best_score = score
            return best_action
                
                

            
def main():
    NoughtsAndCrossesScreen()

if __name__ == "__main__":
    main()

        

                                                                            
