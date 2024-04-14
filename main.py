import tkinter as tk
from tkinter import messagebox
import random

class OXGame:
    """This class represents the game logic of OX Game."""
    PLAYER = "P"
    NPC = "N"

    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        """Resets the game to start a new game."""
        self.board_values = [random.choice(range(1, 100)) for _ in range(9)]
        self.board_state = [-1 for _ in range(9)]
        self.lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        if sum(self.board_values) % 2 == 0:
            self.board_values[0] -= 1
        
        self.player_turn = random.choice([0, 1])
        self.npc_turn = self.player_turn ^ 1
        self.player_score = 0
        self.npc_score = 0

    def is_finished(self, turn):
        """Checks if the game is finished, returning 1 for player win, -1 for NPC win, or 0 to continue."""
        for line in self.lines:
            if self.board_state[line[0]] == self.board_state[line[1]] == self.board_state[line[2]]:
                winner = self.board_state[line[0]]
                if winner == self.PLAYER:
                    return 1
                elif winner == self.NPC:
                    return -1
        
        if turn == 9:
            if self.player_score > self.npc_score:
                return 1
            else:
                return -1
        return 0
        
    def start_npc_turn(self, turn):
        """Determines the NPC's move."""
        result = self.evaluate_position(turn, self.board_state)
        return result[1]
        
    def update(self, idx, user):
        """Updates the game board and scores based on the user's move."""
        if user == self.PLAYER:
            self.player_score += self.board_values[idx]
            self.board_state[idx] = self.PLAYER
        elif user == self.NPC:
            self.npc_score += self.board_values[idx]
            self.board_state[idx] = self.NPC
        
    def evaluate_position(self, turn, board_state):
        """Evaluates the board position using a minimax-like strategy for the NPC."""
        for i in self.lines:
            if board_state[i[0]] == board_state[i[1]] == board_state[i[2]] == self.NPC:
                return [10**18,9]
            elif board_state[i[0]] == board_state[i[1]] == board_state[i[2]] == self.PLAYER:
                return [-10**18,9]
        
        if turn == 9:
            palyer_score,npc_score = 0,0
            for i in range(9):
                if board_state[i] == self.PLAYER:
                    palyer_score += self.board_values[i]
                else:
                    npc_score += self.board_values[i]
            return [npc_score - palyer_score,9]
        
        best_result = [-float("inf"), 9] if turn % 2 == self.npc_turn else [float("inf"), 9]
        for i in range(9):
            if board_state[i] == -1:
                new_board_state = board_state[:]
                new_board_state[i] = self.NPC if turn % 2 == self.npc_turn else self.PLAYER
                result = self.evaluate_position(turn + 1, new_board_state)
                
                if (turn % 2 == self.npc_turn and result[0] > best_result[0]) or (turn % 2 != self.npc_turn and result[0] < best_result[0]):
                    best_result = [result[0], i]

        return best_result

class OXGameGUI:
    """This class represents the graphical user interface for OX Game."""
    def __init__(self):
        self.setup_gui()

    def setup_gui(self):
        """Initializes the GUI components."""
        self.game = OXGame()
        self.turn = 0
        self.root = tk.Tk()
        self.root.title("OX Game")
        self.root.geometry("600x600")
        
        self.turn_frame = tk.Frame(self.root)
        turn_text = "プレイヤーのターン" if self.game.player_turn == 0 else "NPCのターン"
        self.turn_label = tk.Label(self.turn_frame, text=turn_text, font=("Helvetica", 14))
        self.turn_label.pack()
        self.turn_frame.pack()
            
        self.score_frame = tk.Frame(self.root)
        self.player_score_label = tk.Label(self.score_frame, text="プレイヤーのスコア\n0", bg='#FFCCCC', font=("Helvetica", 14), width=25)
        self.npc_score_label = tk.Label(self.score_frame, text="NPCのスコア\n0", bg='#CCDDFF', font=("Helvetica", 14), width=25)
        self.player_score_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.npc_score_label.pack(side=tk.RIGHT, padx=10, pady=10)
        self.score_frame.pack(pady=10)
        
        self.board_frame = tk.Frame(self.root)
        self.board_buttons = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text=self.game.board_values[i*3+j], height=4, width=8, font=("Helvetica", 18))
                button.config(command=lambda i=i, j=j: self.on_player_click(i, j))
                button.grid(row=i, column=j)
                self.board_buttons[i][j] = button

        self.board_frame.pack(pady=10)
        
        self.clicked = None
        
        if self.game.player_turn == 1:
            self.change_button_states("disabled")
        
        self.root.after(1000, self.continue_game)
        self.root.mainloop()

    def on_player_click(self, row, col):
        """Handles player's click on the board."""
        self.clicked = (row, col)
        self.change_button_states("disabled")
        
    def continue_game(self):
        """Continues the game with NPC moves and checks for game end."""
        if self.turn % 2 == self.game.player_turn:
            if self.clicked:
                self.game.update(self.clicked[0] * 3 + self.clicked[1], OXGame.PLAYER)
                self.update_display()
                self.change_button_states("disabled")
                self.turn += 1
        else:
            idx = self.game.start_npc_turn(self.turn)
            self.game.update(idx, OXGame.NPC)
            self.clicked = None
            self.update_display()
            self.change_button_states("normal")
            self.turn += 1

        self.root.update()

        result = self.game.is_finished(self.turn)    
        if result != 0:
            self.root.after_cancel(self.id_)
            if result == 1:
                self.show_result("プレイヤーの勝利です。")
            elif result == -1:
                self.show_result("プレイヤーの負けです。")
        else:
            if self.turn % 2 == self.game.player_turn:
                self.id_ = self.root.after(100, self.continue_game)
            else:
                self.id_ = self.root.after(1000, self.continue_game)

    def update_display(self):
        """Updates the GUI display based on the game state."""
        for i in range(3):
            for j in range(3):
                button = self.board_buttons[i][j]
                state = self.game.board_state[i*3+j]
                if state == OXGame.PLAYER:
                    button.config(bg="red", state=tk.DISABLED)
                elif state == OXGame.NPC:
                    button.config(bg="blue", state=tk.DISABLED)

        self.player_score_label["text"] = f"プレイヤーのスコア\n{self.game.player_score}"
        self.npc_score_label["text"] = f"NPCのスコア\n{self.game.npc_score}"
        turn_text = "プレイヤーのターン" if self.game.player_turn != self.turn % 2 else "NPCのターン"
        self.turn_label["text"] = turn_text

    def change_button_states(self, state):
        """Changes the state of all board buttons."""
        if state == "disabled":    
            for i in range(3):
                for j in range(3):
                    self.board_buttons[i][j].config(state=tk.DISABLED)
        else:
            for i in range(3):
                for j in range(3):
                    if self.game.board_state[i*3+j] == -1:
                        self.board_buttons[i][j].config(state=tk.NORMAL)
            

    def show_result(self, message):
        """Displays the game result and provides options to retry or exit."""
        messagebox.showinfo("リザルト", message)
        self.show_retry_exit_options()

    def show_retry_exit_options(self):
        """Creates a window with options to retry or exit the game."""
        options_window = tk.Toplevel(self.root)
        options_window.title("メニュー")
        options_window.geometry("250x200")

        retry_button = tk.Button(options_window, text="もう一度遊ぶ", command=lambda: [options_window.destroy(),self.root.destroy(), self.setup_gui()], width=15, font=("Helvetica", 14))
        retry_button.pack(pady=5)

        exit_button = tk.Button(options_window, text="終了する", command=self.root.destroy, width=15, font=("Helvetica", 14))
        exit_button.pack(pady=5)

def main():
    game_gui = OXGameGUI() 
    
if __name__ == "__main__":
    main()
