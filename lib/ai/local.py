class LocalSnake(object):

    def whois(self, payload):
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


class BradSnake(object):

    def whois(self, payload):
        return {
            'name': 'BradSnake',
            'color': '#f0f088',
            'head': 'barf'
        }

    def start(self, payload):
        return {
            'taunt': 'go taunt yourself'
        }

    def move(self, payload):
        return {
            'move': 'north',
            'taunt': 'up up and away!'
        }

    def end(self, payload):
        return {
            'taunt': 'barf I died'
        }


LOCAL_SNAKES = {
    'brad': BradSnake
}
