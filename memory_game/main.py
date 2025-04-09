from gpiozero import Button, LED
import atexit
import time
import logging

logging.basicConfig(level=logging.INFO)

class Main:
    """ Main class program """

    def __init__(self, init_delay = 0, loop_delay = 0):
        """ Insance fields definition """
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

        time.sleep(self._init_delay)

    def _setup(self):
        """ Setup function (Will execute only one time) """
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

    def _loop(self):
        """ Loop function (Will execute every tick) """

    def _exit(self):
        """ Clean up function (Will execute when program exits) """
        logging.info("Exiting program")
        self._reset()

    def _greenButtonEvent(self, state):
        """ Callback function when green button is pressed """
        if state:
            logging.info("Green button activated")
            self._greenLed.on()
        else:
            logging.info("Green button deactivated")
            self._greenLed.off()

    def _redButtonEvent(self, state):
        """ Callback function when red button is pressed """
        if state:
            logging.info("Red button activated")
            self._redLed.on()
        else:
            logging.info("Red button deactivated")
            self._redLed.off()

    def _yellowButtonEvent(self, state):
        """ Callback function when yellow button is pressed """
        if state:
            logging.info("Yellow button activated")
            self._yellowLed.on()
        else:
            logging.info("Yellow button deactivated")
            self._yellowLed.off()

    def _blueButtonEvent(self, state):
        """ Callback function when blue button is pressed """
        if state:
            logging.info("Blue button activated")
            self._blueLed.on()
        else:
            logging.info("Blue button deactivated")
            self._blueLed.off()


    def _resetButtonEvent(self, state):
        """ Callback function when reset button is pressed """
        if state:
            logging.info("Reset button activated")
            self._reset()

    def _reset(self):
        """ Reset function """
        logging.info("Resetting states")
        self._greenLed.off()
        self._redLed.off()
        self._blueLed.off()
        self._yellowLed.off()

    def start(self):
        """ Entrypoint of the program """
        try:
            atexit.register(self._exit)
            self._setup()
            time.sleep(self._init_delay)
            logging.info("Starting loop")
            while True:
                self._loop()
                time.sleep(self._loop_delay)
        except (KeyboardInterrupt, SystemExit):
            self._exit()
        finally:
            self._exit()

def main():
    """ Global function to initiate the module (used for setup.py as an enttry point) """
    Main(init_delay=1, loop_delay=0.025).start()

if __name__ == "__main__":
    main()