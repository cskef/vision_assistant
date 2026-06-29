class Speaker:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.engine = None

        if not enabled:
            return

        try:
            import pyttsx3

            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 165)
        except Exception:
            self.engine = None

    def say(self, message):
        print(f"[ALERTE] {message}")
        if not self.enabled or self.engine is None:
            return
        self.engine.say(message)
        self.engine.runAndWait()

    def close(self):
        if self.engine is not None:
            self.engine.stop()

