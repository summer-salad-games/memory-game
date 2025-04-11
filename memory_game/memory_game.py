from gpiozero import Button, LED, Buzzer
import time
import logging

logging.basicConfig(level=logging.INFO)

class MemoryGame:
    def __init__(self, init_delay = 0, loop_delay = 0):
        logging.info("Initializing program")
        self._init_delay = init_delay
        self._loop_delay = loop_delay
        
        self._greenButton = Button(22)
        self._redButton = Button(5)
        self._blueButton = Button(6)
        self._yellowButton = Button(26)
        self._resetButton = Button(13)

        self._greenLed = LED(23)
        self._redLed = LED(24)
        self._blueLed = LED(25)
        self._yellowLed = LED(12)

        self._buzzer = Buzzer(17)

        time.sleep(self._init_delay)

    def _setup(self):
        logging.info("Setting up program")

        self._greenButton.when_activated = lambda: self._greenButtonEvent(True)
        self._greenButton.when_deactivated = lambda: self._greenButtonEvent(False)

        self._redButton.when_activated = lambda: self._redButtonEvent(True)
        self._redButton.when_deactivated = lambda: self._redButtonEvent(False)

        self._blueButton.when_activated = lambda: self._blueButtonEvent(True)
        self._blueButton.when_deactivated = lambda: self._blueButtonEvent(False)

        self._yellowButton.when_activated = lambda: self._yellowButtonEvent(True)
        self._yellowButton.when_deactivated = lambda: self._yellowButtonEvent(False)

        self._resetButton.when_activated = lambda: self._resetButtonEvent(True)
        self._resetButton.when_deactivated = lambda: self._resetButtonEvent(False)

    def _loop(self):
        """ Loop function """

    def _exit(self):
        logging.info("Exiting program")
        self._reset()

    def _greenButtonEvent(self, state):
        if state:
            logging.info("Green button activated")
            self._greenLed.on()
        else:
            logging.info("Green button deactivated")
            self._greenLed.off()

    def _redButtonEvent(self, state):
        if state:
            logging.info("Red button activated")
            self._redLed.on()
        else:
            logging.info("Red button deactivated")
            self._redLed.off()

    def _yellowButtonEvent(self, state):
        if state:
            logging.info("Yellow button activated")
            self._yellowLed.on()
        else:
            logging.info("Yellow button deactivated")
            self._yellowLed.off()

    def _blueButtonEvent(self, state):
        if state:
            logging.info("Blue button activated")
            self._blueLed.on()
        else:
            logging.info("Blue button deactivated")
            self._blueLed.off()

    def _resetButtonEvent(self, state):
        self._reset()

    def _reset(self):
        logging.info("Resetting states")
        self._greenLed.off()
        self._redLed.off()
        self._blueLed.off()
        self._yellowLed.off()
        self._buzzer.off()

    def start(self):
        logging.info("Starting program")
        try:
            self._setup()
            time.sleep(self._init_delay)
            logging.info("Starting loop")
            while True:
                self._loop()
                time.sleep(self._loop_delay)
        except (KeyboardInterrupt, SystemExit):
            logging.info("Program interrupted")
        finally:
            self._exit()