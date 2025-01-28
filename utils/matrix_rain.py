### utils/matrix_rain.py
import os
import random
import time

class MatrixRain:
    def __init__(self):
        self.width = os.get_terminal_size().columns
        self.height = os.get_terminal_size().lines
        self.drops = [0] * self.width
        self.chars = list("aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789@#$%^&*()[]{}<>?/\\|~`!%^&*()-_=+;:'\",.")
    
    def _clear_screen(self):
        print("\033[2J", end='')
    
    def _print_at(self, row, col, char):
        print(f"\033[{row};{col}H{char}", end='')
    
    def animate(self, duration=3):
        try:
            start_time = time.time()
            print("\033[?25l")  # Hide cursor
            while time.time() - start_time < duration:
                self._clear_screen()
                for i in range(self.width):
                    if self.drops[i] > 0:
                        for j in range(3):  # Print multiple characters in each vertical line
                            if self.drops[i] - j > 0:
                                self._print_at(self.drops[i] - j, i + 1, f"\033[32m{random.choice(self.chars)}\033[0m")
                        self.drops[i] += 1
                        if self.drops[i] > self.height or random.random() < 0.05:
                            self.drops[i] = 0
                    elif random.random() < 0.1:  # Increased probability for more vertical lines
                        self.drops[i] = 1
                time.sleep(0.05)  # Reduced sleep time for less space between characters
        except:
            pass
        finally:
            print("\033[?25h")  # Show cursor
            self._clear_screen()
