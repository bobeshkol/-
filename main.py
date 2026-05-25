
from tkinter import messagebox
import random
from modelgame import ShipModel, size, shipshapes, Ship
from visualmodel import ShipVisual


class ShipController:
    def __init__(self):
        self.view = ShipVisual()
        self.model = ShipModel()
        self.placement_phase = True
        self.ships_to_place = shipshapes.copy()
        self.current_ship_idx = 0
        self.placement_direction = 'H'
        self.my_turn = True
        self.setup_bindings()
        self.update_placement_status()

    def setup_bindings(self):
        self.view.dir_button.config(command=self.toggle_direction)

        for y in range(size):
            for x in range(size):
                self.view.my_buttons[y][x].config(
                    bg="#2c3e50",
                    command=lambda cx=x, cy=y: self.my_place_click(cx, cy)
                )
                self.view.enemy_buttons[y][x].config(
                    bg="#341f21",
                    state="disabled",
                    command=lambda cx=x, cy=y: self.my_shoot(cx, cy)
                )

    def toggle_direction(self):
        self.placement_direction = 'V' if self.placement_direction == 'H' else 'H'
        self.view.dir_button.config(text=f"Поворот: {'Верт' if self.placement_direction == 'V' else 'Гор'}")

    def update_placement_status(self):
        if self.current_ship_idx < len(self.ships_to_place):
            length = self.ships_to_place[self.current_ship_idx]
            self.view.status_label.config(text=f"🛠 Розстановка\n\nПоставте\n{length}-палубний корабель", fg="#4da8da")
            rem = self.ships_to_place[self.current_ship_idx:]
            self.view.info_label.config(
                text=f"Залишилось:\n4-пал: {rem.count(4)}  3-пал: {rem.count(3)}\n2-пал: {rem.count(2)}  1-пал: {rem.count(1)}")
        else:
            self.placement_phase = False
            self.view.dir_button.pack_forget()
            self.view.info_label.config(text="🚢 Флот готовий!", font=("Arial", 10, "bold"), fg="#2ecc71")
            for y in range(size):
                for x in range(size):
                    self.view.enemy_buttons[y][x].config(state="normal")
            self.view.status_label.config(text="🎯 Ваш хід!\n\nСтріляйте по ворогу!", fg="white")

    def my_place_click(self, x, y):
        if not self.placement_phase:
            return
        length = self.ships_to_place[self.current_ship_idx]
        if self.model.availableplace(self.model.my_field, x, y, length, self.placement_direction):
            coordinates = []
            for i in range(length):
                nx, ny = (x + i, y) if self.placement_direction == 'H' else (x, y + i)
                self.model.my_field[ny][nx] = 1
                coordinates.append((nx, ny))
                self.view.my_buttons[ny][nx].config(bg="#95a5a6", text="🚢", fg="#2c3e50")

            self.model.my_ships.append(Ship(coordinates))
            self.current_ship_idx += 1
            self.update_placement_status()
        else:
            messagebox.showwarning("Помилка", "Сюди не можна ставити корабель за правилами окруження!")

    def update_ui(self):
        for y in range(size):
            for x in range(size):
                val_p = self.model.my_field[y][x]
                if val_p == 2:
                    self.view.my_buttons[y][x].config(bg="#34495e", text="✖", fg="#4da8da")
                elif val_p == 3:
                    self.view.my_buttons[y][x].config(bg="#e74c3c", text="🔥", fg="white")
                elif val_p == 4:
                    self.view.my_buttons[y][x].config(bg="#000000", text="☠️", fg="white")
                val_e = self.model.enemy_field[y][x]
                if val_e == 2:
                    self.view.enemy_buttons[y][x].config(bg="#2c2c2c", text="✖", fg="#e74c3c")
                elif val_e == 3:
                    self.view.enemy_buttons[y][x].config(bg="#d35400", text="🔥", fg="white")
                elif val_e == 4:
                    self.view.enemy_buttons[y][x].config(bg="#000000", text="☠️", fg="white")

    def my_shoot(self, x, y):
        if not self.my_turn or self.placement_phase:
            return
        if self.model.enemy_field[y][x] in [2, 3, 4]:
            return

        result, ship = self.model.mark_shot(self.model.enemy_field, self.model.enemy_ships, x, y)
        self.update_ui()

        if result == 'miss':
            self.my_turn = False
            self.view.status_label.config(text="🤖 Хід комп'ютера...", fg="#ff4d4d")
            self.view.after(1000, self.ai_shoot)
        elif result in ['hit', 'sink']:
            if self.model.check_victory(self.model.enemy_field):
                messagebox.showinfo("Перемога!", "Вітаємо! Ви повністю розгромили ворожий флот!")
                self.view.status_label.config(text="🏆 Ви перемогли!", fg="#2ecc71")
                self.disable_all_enemy_buttons()

    def ai_shoot(self):
        if self.placement_phase:
            return
        available_shots = [(x, y) for y in range(size) for x in range(size) if self.model.my_field[y][x] in [0, 1]]
        if not available_shots:
            return
        x, y = random.choice(available_shots)
        result, ship = self.model.mark_shot(self.model.my_field, self.model.my_ships, x, y)
        self.update_ui()
        if result == 'miss':
            self.my_turn = True
            self.view.status_label.config(text="🎯 Ваш хід!\n\nСтріляйте по ворогу!", fg="white")
        elif result in ['hit', 'sink']:
            if self.model.check_victory(self.model.my_field):
                messagebox.showinfo("Поразка", "Комп'ютер знищив усі ваші кораблі!")
                self.view.status_label.config(text="💀 Ви програли!", fg="#e74c3c")
                self.disable_all_enemy_buttons()
            else:
                self.view.after(1000, self.ai_shoot)

    def disable_all_enemy_buttons(self):
        for y in range(size):
            for x in range(size):
                self.view.enemy_buttons[y][x].config(state="disabled")


if __name__ == "__main__":
    game = ShipController()
    game.view.mainloop()