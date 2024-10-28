import tkinter as tk
import numpy as np
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid_size = 4
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.score = 0
        
        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="lightgray")
        self.canvas.pack()
        
        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack()
        
        restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        restart_button.pack()

        self.master.bind("<Key>", self.key_press)

    def start_game(self):
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.update_canvas()

    def restart_game(self):
        self.start_game()

    def add_random_tile(self):
        empty_tiles = list(zip(*np.where(self.board == 0)))
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.board[row][col] = random.choice([2, 4])

    def key_press(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            moved = False
            if event.keysym == 'Up':
                moved = self.move_up()
            elif event.keysym == 'Down':
                moved = self.move_down()
            elif event.keysym == 'Left':
                moved = self.move_left()
            elif event.keysym == 'Right':
                moved = self.move_right()

            if moved:
                self.add_random_tile()
                if not any(self.can_move()):
                    self.game_over()
                self.update_canvas()

    def move_up(self):
        return self.move(np.transpose(self.board), transpose_back=True)

    def move_down(self):
        return self.move(np.flipud(np.transpose(self.board)), transpose_back=True)

    def move_left(self):
        return self.move(self.board)

    def move_right(self):
        return self.move(np.fliplr(self.board))

    def move(self, board, transpose_back=False):
        moved = False
        for i in range(self.grid_size):
            original_row = board[i].copy()
            new_row = [x for x in original_row if x!= 0]
            merged_row = []
            skip = False
            
            for j in range(len(new_row)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(new_row) and new_row[j] == new_row[j + 1]:
                    merged_row.append(new_row[j] * 2)
                    self.score += new_row[j] * 2
                    skip = True
                else:
                    merged_row.append(new_row[j])
            
            merged_row += [0] * (self.grid_size - len(merged_row))
            board[i] = np.array(merged_row)
            
            if not np.array_equal(original_row, board[i]):
                moved = True
        
        if transpose_back:
            board = np.transpose(board) if 'up' in self.move.__code__.co_varnames else np.transpose(np.flipud(board))
            for i, row in enumerate(board):
                self.board[i] = row
        else:
            for i, row in enumerate(board):
                self.board[i] = row
        
        return moved

    def can_move(self):
        # Check horizontally
        for row in self.board:
            for j in range(self.grid_size - 1):
                if row[j] == 0 or row[j] == row[j + 1]:
                    yield True
        # Check vertically
        for col in np.transpose(self.board):
            for j in range(self.grid_size - 1):
                if col[j] == 0 or col[j] == col[j + 1]:
                    yield True
        yield False  # Ensures at least one value is always yielded

    def game_over(self):
        print("Game Over! Final Score:", self.score)
        # Optional: Display game over on the GUI
        self.canvas.delete("all")
        self.canvas.create_text(200, 200, text="Game Over!", font=("Arial", 24))

    def update_canvas(self):
        self.canvas.delete("all")
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = int(self.board[i][j])
                x0, y0, x1, y1 = j * 100 + 5, i * 100 + 5, j * 100 + 95, i * 100 + 95
                
                color_map = {
                    0: "lightgray",
                    2: "orange",
                    4: "yellow",
                    8: "green",
                    16: "blue",
                    # Add more colors for higher values as needed
                }
                
                color = color_map.get(value, "purple") # Default color for values >16
                
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                if value!= 0:
                    self.canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(value), font=("Arial", 24))

        self.score_label.config(text=f"Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game_2048 = Game2048(root)
    root.mainloop()