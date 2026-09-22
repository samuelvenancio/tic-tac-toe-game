from tkinter import *
from tkinter import ttk, messagebox

class TicTacToe:

    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe Game")
        self.root.configure(bg="#f5f0e8")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Shell.TFrame", background="#f5f0e8")
        style.configure("Board.TFrame", background="#263238")
        style.configure("Title.TLabel", background="#f5f0e8", foreground="#263238", font=("Helvetica", 24, "bold"))
        style.configure("Turn.TLabel", background="#f5f0e8", foreground="#546e7a", font=("Helvetica", 13, "bold"))
        style.configure("Cell.TButton", font=("Helvetica", 36, "bold"), foreground="#263238", background="#ffffff", padding=20)
        style.map(
            "Cell.TButton",
            background=[("disabled", "#ffffff"), ("active", "#e8f5e9")],
            foreground=[("disabled", "#263238")],
        )
        style.configure("Restart.TButton", font=("Helvetica", 11, "bold"), padding=(18, 10), foreground="#ffffff", background="#00897b")
        style.map("Restart.TButton", background=[("active", "#00695c")])

        mainframe = ttk.Frame(root, padding=(28, 24, 28, 28), style="Shell.TFrame")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.player = StringVar()
        self.player.set("Player 1")
        self.turn_text = StringVar()
        self.player.trace_add("write", self.update_turn_text)
        self.update_turn_text()

        ttk.Label(mainframe, text="Tic Tac Toe", style="Title.TLabel").grid(row=0, column=0, sticky=W)
        ttk.Label(mainframe, textvariable=self.turn_text, style="Turn.TLabel").grid(row=1, column=0, sticky=W, pady=(4, 18))

        board = ttk.Frame(mainframe, padding=8, style="Board.TFrame")
        board.grid(row=2, column=0, sticky=(N, W, E, S))

        self.matrix = []
        for i in range(3):
            self.matrix.append([])
            board.rowconfigure(i, weight=1, minsize=110)
            board.columnconfigure(i, weight=1, minsize=110)
            for j in range(3):
                button = ttk.Button(board, style="Cell.TButton", command=lambda row_index=i, col_index=j: self.change(row_index, col_index))
                self.matrix[i].append(button)
                button.grid(row=i, column=j, sticky="snew", padx=4, pady=4)

        ttk.Button(mainframe, text="Restart game", style="Restart.TButton", command=self.restart).grid(row=3, column=0, sticky=E, pady=(18, 0))

    def update_turn_text(self, *args):
        mark = "X" if self.player.get() == "Player 1" else "O"
        self.turn_text.set(f"{self.player.get()}'s turn ({mark})")

    def change(self, row_index, col_index):
        player = self.player.get()
        button = self.matrix[row_index][col_index]
        symbol = "X" if player == "Player 1" else "O"
        self.board[row_index][col_index] = symbol
        button.config(text=symbol, state="disabled")
        checked = self.check_if_player_won(row_index, col_index, symbol)
        if checked:
            self.gameover(player)
        elif self.is_board_full():
            self.tie()
        else:
            self.switch_player()

    def check_if_player_won(self, row_index, col_index, symbol) -> bool:
        if all(self.board[row_index][j] == symbol for j in range(3)):
            return True
        if all(self.board[i][col_index] == symbol for i in range(3)):
            return True
        if row_index == col_index:
            if all(self.board[i][i] == symbol for i in range(3)):
                return True
        if row_index + col_index == 2:
            if all(self.board[i][2 - i] == symbol for i in range(3)):
                return True
        return False

    def is_board_full(self):
        return all(item != "" for row in self.board for item in row)

    def switch_player(self):
        if self.player.get() == "Player 1":
            self.player.set("Player 2")
        else:
            self.player.set("Player 1")

    def restart(self):
        self.player.set("Player 1")
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ""
                button = self.matrix[i][j] 
                button.configure(text="", state="normal")

    def gameover(self, winner):
        messagebox.showinfo("Game Over", f"{winner} won!")
        self.restart()

    def tie(self):
        messagebox.showinfo("Game Over", "The game ended in a draw")
        self.restart()
        
root = Tk()
TicTacToe(root)
root.mainloop()
