# game_logic.py

import time
import random
import config

class Game:

    def __init__(self, display, inputs, lights):
        self.display = display
        self.inputs = inputs
        self.lights = lights

        self.state = config.STATE_MENU
        self.diff = config.DEFAULT_DIFFICULTY_INDEX

        self.level = 1
        self.sequence = []
        self.step = 0
        self.deadline = 0

        self.display.show_menu(config.DIFFICULTIES, self.diff)
        self.lights.set_idle()

    # ================= MENU =================
    def update(self, now):
        if self.state == config.STATE_MENU:
            self.update_menu()
        elif self.state == config.STATE_PLAYING:
            self.update_play(now)
        elif self.state in (config.STATE_GAME_OVER, config.STATE_WIN):
            if self.inputs.get_press():
                self.goto_menu()

    def update_menu(self):
        if self.inputs.get_turn():
            self.diff = (self.diff + 1) % len(config.DIFFICULTIES)
            self.display.show_menu(config.DIFFICULTIES, self.diff)

        if self.inputs.get_press():
            self.start_game()

    # ================= GAME FLOW =================
    def start_game(self):
        self.level = 1
        self.next_level()
        self.lights.game_start()

    def next_level(self):
        if self.level > config.LEVEL_COUNT:
            self.display.show_win()
            self.state = config.STATE_WIN
            self.lights.win()
            return

        self.state = config.STATE_PLAYING
        self.sequence = self.generate_sequence()
        self.step = 0

        diff = config.DIFFICULTIES[self.diff]
        start = diff["time_start"]
        end = diff["time_end"]
        t = start - (start - end) * ((self.level - 1) / (config.LEVEL_COUNT - 1))
        self.time_per_step = t

        self.deadline = time.monotonic() + self.time_per_step
        self.show_step()

    # ================= SEQUENCE GEN =================
    def generate_sequence(self):
        length = config.DIFFICULTIES[self.diff]["base_sequence_length"]
        seq = []
        last_tilt = None

        for _ in range(length):
            a = random.choice(config.ACTIONS)

            while (
                a in config.TILT_ACTIONS
                and a == last_tilt
            ):
                a = random.choice(config.ACTIONS)

            seq.append(a)
            if a in config.TILT_ACTIONS:
                last_tilt = a

        return seq

    def show_step(self):
        action = self.sequence[self.step]
        text = config.ACTION_LABELS[action]
        self.display.show_level(self.level, self.step, len(self.sequence), action, text)

    # ================= PLAYING =================
    def update_play(self, now):
        if now > self.deadline:
            self.fail()
            return

        a = self.sequence[self.step]

        # TURN
        if self.inputs.get_turn():
            if a == config.ACTION_ROTATE:
                self.success()
            else:
                self.fail()
            return

        # PRESS
        if self.inputs.get_press():
            if a == config.ACTION_PRESS:
                self.success()
            else:
                self.fail()
            return

        # TILT
        tilt = self.inputs.get_tilt()
        if tilt:
            if tilt == a:
                self.success()
            else:
                self.fail()

    # ================= SUCCESS / FAIL =================
    def success(self):
        self.lights.success()
        self.step += 1
        if self.step >= len(self.sequence):
            self.level += 1
            self.next_level()
        else:
            self.deadline = time.monotonic() + self.time_per_step
            self.show_step()

    def fail(self):
        self.state = config.STATE_GAME_OVER
        self.display.show_game_over(self.level)
        self.lights.failure()

    def goto_menu(self):
        self.state = config.STATE_MENU
        self.display.show_menu(config.DIFFICULTIES, self.diff)
        self.lights.set_idle()

