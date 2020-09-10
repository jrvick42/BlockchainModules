class block():
    def __init__(self):
        self.sender = ''
        self.reciever = ''
        self.message = ''
        self.time = 0
        self.nonce = 0
        self.hash = ''
        self.prevHash = ''

    def setSender(self, value):
        self.sender = value
    def setReciever(self, value):
        self.reciever = value
    def setMessage(self, value):
        self.message = value
    def setTime(self, value):
        self.time = value
    def setNonce(self, value):
        self.nonce = value
    def setHash(self, value):
        self.hash = value
    def setPrevHash(self, value):
        self.prevHash = value
