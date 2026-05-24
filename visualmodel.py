import tkinter as tk
letters = ["А", "Б", "В", "Г", "Д", "Е", "Є", "Ж", "З", "И"]
size = 10
class ShipVisual(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Гра Морський Бій")
        self.configure(bg="#2c2c2c") #вбудований метод, який дозволяє змінювати властивості об'єкта після того, як він був створений

        self.my_buttons = [[None] * size for _ in range(size)]
        self.enemy_buttons = [[None] * size for _ in range(size)]

        self.createallvisualelem()

    def creategridplace(self, parent, buttons_matrix, is_player):
        colorcoordinates = "#4da8da" if is_player else "#ff4d4d"
        for i in range(size + 1):
            parent.grid_columnconfigure(i, minsize=45, weight=1)

        for x in range(size):
            tk.Label(parent, text=letters[x], font=("Arial", 10, "bold"),
                     bg="#1e1e24", fg=colorcoordinates).grid(row=0, column=x + 1, sticky="nsew")

        for y in range(size):
            tk.Label(parent, text=str(y + 1), font=("Arial", 10, "bold"),
                     bg="#1e1e24", fg=colorcoordinates).grid(row=y + 1, column=0, sticky="nsew")
            for x in range(size):
                btn = tk.Button(parent, width=4, height=2, relief="flat", bd=1)
                btn.grid(row=y + 1, column=x + 1, sticky="nsew", padx=1, pady=1)
                buttons_matrix[y][x] = btn

    def createallvisualelem(self):
        self.main_frame = tk.Frame(self, bg="#1e1e24")
        self.main_frame.pack(padx=20, pady=20)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, minsize=220)
        self.main_frame.grid_columnconfigure(2, weight=1)

        self.my_frame = tk.LabelFrame(self.main_frame, text="Ваше поле", bg="#1e1e24", fg="#4da8da", font=("Arial", 11, "bold"))
        self.my_frame.grid(row=0, column=0, sticky="n", padx=10)
        self.creategridplace(self.my_frame, self.my_buttons, True)

        self.center_frame = tk.Frame(self.main_frame, bg="#1e1e24")
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        self.control_frame = tk.Frame(self.center_frame, bg="#2a2a35", highlightbackground="#4da8da", highlightthickness=1)
        self.control_frame.pack(fill="x", pady=(20, 10))

        self.dir_button = tk.Button(self.control_frame, text="Горизонтальне положення", font=("Arial", 9, "bold"), bg="#34495e", fg="white")
        self.dir_button.pack(pady=10, padx=10, fill="x")

        self.info_label = tk.Label(self.control_frame, text="", bg="#2a2a35", fg="white", font=("Arial", 9), justify="left")
        self.info_label.pack(pady=5)

        self.status_label = tk.Label(self.center_frame, text="", font=("Arial", 11, "bold"), bg="#2a2a35", fg="#ffffff", wraplength=200, height=6, relief="groove")
        self.status_label.pack(fill="x", pady=10)

        self.enemy_frame = tk.LabelFrame(self.main_frame, text="Поле ворога", bg="#1e1e24", fg="#ff4d4d", font=("Arial", 11, "bold"))
        self.enemy_frame.grid(row=0, column=2, sticky="n", padx=10)
        self.creategridplace(self.enemy_frame, self.enemy_buttons, False)
if __name__ == "__main__":
    app = ShipVisual()
    app.mainloop()