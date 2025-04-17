import logging
import random
import time

from gpiozero import LED, RGBLED, Button, Buzzer

logging.basicConfig(level=logging.INFO)


class Main:

    def __init__(self, init_delay=0, loop_delay=0):
        logging.info("Initializing program")

        self._init_delay = init_delay
        self._loop_delay = loop_delay

        self._green_button = Button(22, bounce_time=0.1)
        self._red_button = Button(5, bounce_time=0.1)
        self._blue_button = Button(6, bounce_time=0.1)
        self._yellow_button = Button(26, bounce_time=0.1)
        self._reset_button = Button(13, bounce_time=0.1)

        self._green_led = LED(23)
        self._red_led = LED(24)
        self._blue_led = LED(25)
        self._yellow_led = LED(12)

        self._rgb_led = RGBLED(16, 21, 20, active_high=False, initial_value=(0, 0, 0))

        self._buzzer = Buzzer(17)

        self._possible_colors = ["red", "green", "blue", "yellow"]
        self._role = "machine"
        self._is_game_ready = False
        self._colors_to_remember = []
        self._turn = 0

        time.sleep(self._init_delay)

    def _setup(self):
        logging.info("Setting up program")

        self._green_button.when_activated = lambda: self._button_event(
            True, self._green_led, "green"
        )
        self._green_button.when_deactivated = lambda: self._button_event(
            False, self._green_led, "green"
        )

        self._red_button.when_activated = lambda: self._button_event(
            True, self._red_led, "red"
        )
        self._red_button.when_deactivated = lambda: self._button_event(
            False, self._red_led, "red"
        )

        self._blue_button.when_activated = lambda: self._button_event(
            True, self._blue_led, "blue"
        )
        self._blue_button.when_deactivated = lambda: self._button_event(
            False, self._blue_led, "blue"
        )

        self._yellow_button.when_activated = lambda: self._button_event(
            True, self._yellow_led, "yellow"
        )
        self._yellow_button.when_deactivated = lambda: self._button_event(
            False, self._yellow_led, "yellow"
        )

        self._reset_button.when_activated = lambda: self._reset_button_event(True)
        self._reset_button.when_deactivated = lambda: self._reset_button_event(False)

        self._start_game()

    def _start_game(self):
        logging.info("Starting game")

        self._reset()
        self._play_init_sequence()
        time.sleep(2)
        self._add_color_to_remember()

    def _loop(self):
        time.sleep(self._loop_delay)

    def _exit(self):
        logging.info("Exiting program")
        self._reset()

    def _play_color_sequence(self):
        logging.info(f"Playing color sequence {self._colors_to_remember}")

        for color in self._colors_to_remember:
            if color == "red":
                self._red_led.on()
            elif color == "green":
                self._green_led.on()
            elif color == "blue":
                self._blue_led.on()
            elif color == "yellow":
                self._yellow_led.on()

            time.sleep(0.5)

            self._red_led.off()
            self._green_led.off()
            self._blue_led.off()
            self._yellow_led.off()

            time.sleep(0.5)

    def _add_color_to_remember(self):
        self._set_role("machine")
        new_color = random.choice(self._possible_colors)
        logging.info(f"Adding color {new_color} to remember list")
        self._colors_to_remember.append(new_color)
        self._play_color_sequence()
        self._set_role("user")

    def _set_role(self, role):
        logging.info(f"Setting role to {role}")
        self._role = role
        self._play_buzzer()
        if role == "machine":
            self._rgb_led.value = (1, 0, 0)
        elif role == "user":
            self._rgb_led.value = (0, 1, 0)

    def _play_init_sequence(self):
        logging.info("Starting initialization sequence")
        delay = 0.15

        led_sequence = [
            self._green_led,
            self._red_led,
            self._blue_led,
            self._yellow_led,
        ]
        reversed_led_sequence = led_sequence[::-1]

        self._rgb_led.pulse(
            on_color=(0, 1, 0), off_color=(1, 0, 0), fade_in_time=0.5, fade_out_time=0.5
        )

        self._bounce_leds(led_sequence)
        time.sleep(delay)
        self._bounce_leds(reversed_led_sequence)
        time.sleep(delay)
        self._bounce_leds(led_sequence)
        time.sleep(delay)
        self._bounce_leds(reversed_led_sequence)

        self._rgb_led.off()

        self._blue_led.on()
        self._red_led.on()
        self._yellow_led.on()
        self._green_led.on()
        self._rgb_led.value = (1, 0, 0)
        self._play_buzzer()
        self._blue_led.off()
        self._red_led.off()
        self._yellow_led.off()
        self._green_led.off()
        self._rgb_led.off()
        time.sleep(delay)
        self._blue_led.on()
        self._red_led.on()
        self._yellow_led.on()
        self._green_led.on()
        self._rgb_led.value = (0, 1, 0)
        self._play_buzzer()
        self._blue_led.off()
        self._red_led.off()
        self._yellow_led.off()
        self._green_led.off()
        self._rgb_led.off()
        time.sleep(delay)

        self._is_game_ready = True

    def _play_buzzer(self, duration=0.15):
        self._buzzer.on()
        time.sleep(duration)
        self._buzzer.off()

    def _bounce_leds(self, led_sequence, delay=0.15):
        for led in led_sequence:
            led.on()
            time.sleep(delay)
            led.off()

    def _button_event(self, state, led, color):
        logging.info(f"Button {color} event state {state}")

        if not self._is_game_ready or self._role == "machine":
            logging.info(f"Ignoring {color} button")
            return

        if state:
            led.on()
        else:
            led.off()

        if not state:
            if self._colors_to_remember[self._turn] == color:
                logging.info(f"Correct {color} color pressed")
                self._turn += 1
            else:
                logging.info("Wrong color pressed, game over")
                self._play_game_over_sequence()
                self._start_game()

            if self._turn == len(self._colors_to_remember):
                logging.info("All colors has been guesed")
                time.sleep(0.5)
                self._turn = 0
                self._add_color_to_remember()

    def _play_game_over_sequence(self):
        logging.info("Playing game over sequence")

        self._blue_led.on()
        self._red_led.on()
        self._yellow_led.on()
        self._green_led.on()
        self._rgb_led.value = (1, 0, 0)
        self._play_buzzer()
        self._blue_led.off()
        self._red_led.off()
        self._yellow_led.off()
        self._green_led.off()
        self._rgb_led.off()
        time.sleep(0.15)
        self._blue_led.on()
        self._red_led.on()
        self._yellow_led.on()
        self._green_led.on()
        self._rgb_led.value = (1, 0, 0)
        self._play_buzzer()
        self._blue_led.off()
        self._red_led.off()
        self._yellow_led.off()
        self._green_led.off()
        self._rgb_led.off()
        time.sleep(2)

    def _reset_button_event(self, state):
        if state:
            logging.info("Reset button activated")
            self._start_game()

    def _reset(self):
        logging.info("Resetting states")
        self._green_led.off()
        self._red_led.off()
        self._blue_led.off()
        self._yellow_led.off()
        self._buzzer.off()
        self._rgb_led.off()
        self._colors_to_remember = []
        self._turn = 0
        self._role = "machine"
        self._is_game_ready = False

    def start(self):
        logging.info("Starting program")
        try:
            self._setup()
            time.sleep(self._init_delay)
            logging.info("Starting loop")
            while True:
                self._loop()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Program interrupted")
        finally:
            self._exit()