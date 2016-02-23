class BaseConfigurationStep:
    def __init__(self):
        self.a = 'a'

    def process(self, environment):
        raise Exception('Not implemented. Abstract class usage')
