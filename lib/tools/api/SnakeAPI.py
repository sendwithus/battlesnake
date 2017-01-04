class SnakeAPI(object):
    """ Base object for all Snake AIs """

    def whois(self):
        """ Responds: name, color, head """
        raise NotImplementedError()

    def start(self, payload):
        """ Responds: taunt """
        raise NotImplementedError()

    def move(self, payload):
        """ Responds: move, taunt """
        raise NotImplementedError()

    def end(self, payload):
        """ Responds: taunt """
        raise NotImplementedError()
