import time
import random
import config


class Game:
    def __init__(self, display, inputs, lights):
        # Core managers
        self.display = display
        self.inputs = inputs
        self.lights = lights

        # Global game state
        self.state = config.STATE_MENU
        self.diff = config.DEFAULT_DIFFICULTY_INDEX

        # Level / sequence state
        self.level = 1
        self.sequence = []
        self.step = 0
        self.time_per_step = 5.0
        self.deadline = 0.0

        # 初始显示菜单
        self.display.show_menu(config.DIFFICULTIES, self.diff)
        self.lights.set_idle()

    # ============================
    # Top-level state update
    # ============================
    def update(self, now):
        # 更新灯光动画（用于胜利彩灯效果）
        self.lights.update(now)
        
        if self.state == config.STATE_MENU:
            self.update_menu(now)
        elif self.state == config.STATE_PLAYING:
            self.update_play(now)
        elif self.state == config.STATE_GAME_OVER:
            self.update_game_over(now)
        elif self.state == config.STATE_WIN:
            self.update_win(now)

    # ============================
    # MENU
    # ============================
    def update_menu(self, now):
        # 旋钮切换难度
        if self.inputs.get_turn():
            self.diff = (self.diff + 1) % len(config.DIFFICULTIES)
            self.display.show_menu(config.DIFFICULTIES, self.diff)

        # 按下开始游戏
        if self.inputs.get_press():
            self.start_game()

    def start_game(self):
        self.level = 1
        self.lights.game_start()
        self.next_level()

    # ============================
    # Level / sequence helpers
    # ============================
    def next_level(self):
        # 按当前难度 + 关卡生成序列
        self.sequence = self._build_sequence_for_level()
        self.time_per_step = self._time_for_level()
        self.step = 0
        self.deadline = time.monotonic() + self.time_per_step

        self.state = config.STATE_PLAYING
        self.lights.set_playing()
        self.show_step()

    def _build_sequence_for_level(self):
        """随机生成动作序列，避免连续重复同一个倾斜。"""
        # 从配置中获取当前关卡的序列长度
        lengths = config.DIFFICULTIES[self.diff]["sequence_lengths"]
        length = lengths[self.level - 1]  # level是1-based，列表是0-based

        seq = []
        last_tilt = None

        for _ in range(length):
            a = random.choice(config.ACTIONS)

            # 避免连续两个相同的倾斜动作
            while a in config.TILT_ACTIONS and a == last_tilt:
                a = random.choice(config.ACTIONS)

            seq.append(a)
            if a in config.TILT_ACTIONS:
                last_tilt = a

        return seq

    def _time_for_level(self):
        """
        同一难度下：
        - level 越高，每一步时间越短
        - 在 time_start 和 time_end 之间线性递减
        """
        d = config.DIFFICULTIES[self.diff]
        start = d["time_start"]
        end = d["time_end"]

        # 线性插值：从第1关到第10关，时间从start线性减少到end
        progress = (self.level - 1) / (config.LEVEL_COUNT - 1)  # 0到1之间
        t = start - (start - end) * progress
        
        return t

    def show_step(self):
        action = self.sequence[self.step]
        text = config.ACTION_LABELS[action]
        # step 为 0-based，DisplayManager 内部会显示 step+1
        self.display.show_level(
            self.level,
            self.step,
            len(self.sequence),
            action,
            text,
        )

    # ============================
    # PLAYING
    # ============================
    def update_play(self, now):
        # 超时：直接失败
        if now > self.deadline:
            remaining = now - self.deadline
            expected = self.sequence[self.step]
            print(f"⏰ TIMEOUT! Expected: {expected}, Overdue by: {remaining:.2f}s")
            self.fail()
            return

        expected = self.sequence[self.step]
        
        # 调试：显示剩余时间
        remaining_time = self.deadline - now
        if remaining_time < 1.0:  # 最后1秒显示倒计时
            print(f"⏱️ Time left: {remaining_time:.1f}s, Waiting for: {expected}")

        # ---------- 情况 1：本步需要「倾斜」 ----------
        if expected in config.TILT_ACTIONS:
            current_tilt = self.inputs.get_tilt()
            
            # 调试输出
            if current_tilt is not None:
                if current_tilt == expected:
                    print(f"✅ Correct tilt detected: {current_tilt}")
                else:
                    print(f"❌ Wrong tilt: got {current_tilt}, expected {expected}")

            if current_tilt == expected:
                # 到达正确方向 -> 立刻通过本步
                self._step_success()
            # 如果方向不对（或者 None），不立刻判错，只是继续等
            return

        # ---------- 情况 2：本步是「旋转」 ----------
        if expected == config.ACTION_ROTATE:
            turn = self.inputs.get_turn()
            if turn:
                print(f"✅ Rotate detected")
                self._step_success()
            # 倾斜 / 按压全部忽略（不会判错）
            return

        # ---------- 情况 3：本步是「按压」 ----------
        if expected == config.ACTION_PRESS:
            if self.inputs.get_press():
                print(f"✅ Press detected")
                self._step_success()
            # 倾斜 / 旋转全部忽略
            return

        # 如果走到这里，说明配置里有未知动作，暂时什么都不做，靠超时结束。

    def _step_success(self):
        """当前一步成功，推进到下一步或下一关。"""
        self.lights.success()
        self.step += 1

        # 本关结束 -> 下一关或通关
        if self.step >= len(self.sequence):
            print(f"🎉 Level {self.level} completed!")
            
            # 检查是否通关（完成第10关）
            if self.level >= config.LEVEL_COUNT:
                self.win()
            else:
                self.level += 1
                self.next_level()
        else:
            # 本关下一步
            self.deadline = time.monotonic() + self.time_per_step
            self.show_step()

    # ============================
    # WIN
    # ============================
    def win(self):
        """通关！"""
        self.state = config.STATE_WIN
        self.display.show_win()
        self.lights.win()
        print("🏆 YOU WIN! All levels completed!")

    def update_win(self, now):
        """通关画面，按键返回菜单"""
        if self.inputs.get_press():
            self.goto_menu()

    # ============================
    # GAME OVER
    # ============================
    def fail(self):
        self.state = config.STATE_GAME_OVER
        self.display.show_game_over(self.level)
        self.lights.failure()

    def update_game_over(self, now):
        # 按键返回菜单
        if self.inputs.get_press():
            self.goto_menu()

    # ============================
    # 返回菜单
    # ============================
    def goto_menu(self):
        self.state = config.STATE_MENU
        self.display.show_menu(config.DIFFICULTIES, self.diff)
        self.lights.set_idle()
