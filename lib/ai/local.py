from importlib import import_module


LOCAL_SNAKE_CLASSES = {}


class LocalSnake(object):
    """ Base object for all Local Snakes to inherit from. """

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


def create_local_snake(snake_name):
    # Import Snake class if we don't have it already.
    if snake_name not in LOCAL_SNAKE_CLASSES:
        module_name = 'snakes.%s' % snake_name
        module = import_module(module_name)

        LOCAL_SNAKE_CLASSES[snake_name] = getattr(module, 'Snake')

    return LOCAL_SNAKE_CLASSES[snake_name]()
