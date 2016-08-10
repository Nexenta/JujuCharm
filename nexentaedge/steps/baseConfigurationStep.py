class BaseConfigurationStep:
    def print_step_name(self):
        print('[{}]'.format(self.__class__.__name__))

    def process(self, environment):
        raise Exception('Not implemented. Abstract class usage')
