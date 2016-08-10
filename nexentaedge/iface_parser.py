import os


class NetworkBlock(object):
    keyword = None

    def __init__(self):
        pass

    def render(self):
        raise NotImplementedError()

    def process(self, lines, index):
        raise NotImplementedError()

    def test_comment(self, line):
        return line.startswith('#')


class AnotherBlock(NetworkBlock):
    keyword = None

    def __init__(self):
        super(AnotherBlock, self).__init__()
        self.data = None

    def render(self):
        return self.data

    def process(self, lines, index):
        self.data = lines[index]
        return index + 1


class SourceBlock(NetworkBlock):
    keyword = 'source'

    def __init__(self):
        super(SourceBlock, self).__init__()
        self.file_path = None

    def render(self):
        return '{} {}'.format(self.keyword, self.file_path)

    def process(self, lines, index):
        self.file_path = [s.strip() for s in lines[index].split(' ') if s][-1]
        return index + 1


class SourceDirectoryBlock(NetworkBlock):
    keyword = 'source-directory'

    def __init__(self):
        super(SourceDirectoryBlock, self).__init__()
        self.path = None

    def render(self):
        return '{} {}'.format(self.keyword, self.path)

    def process(self, lines, index):
        self.path = [s.strip() for s in lines[index].split(' ') if s][-1]
        return index + 1


class AutoBlock(NetworkBlock):
    keyword = 'auto'

    def __init__(self):
        super(AutoBlock, self).__init__()
        self.ifaces = []

    def render(self):
        return '{} {}'.format(self.keyword, ' '.join(self.ifaces))

    def process(self, lines, index):
        self.ifaces = [s.strip() for s in lines[index].split(' ') if s][1:]
        return index + 1


class IfaceBlock(NetworkBlock):
    keyword = 'iface'

    def __init__(self):
        super(IfaceBlock, self).__init__()
        self.name = None
        self.address_type = None
        self.service_type = None
        self.params = {}

    def render(self):
        header = '{} {} {} {}'.format(self.keyword, self.name, self.address_type, self.service_type)
        cfg = []
        for key in self.params:
            cfg.append('{} {}'.format(key, self.params[key]))
        return '{}\n{}'.format(header, '\n'.join(map(lambda x: ' '*4 + x, cfg)))

    def process(self, lines, index):
        line = lines[index]
        sp = [s.strip() for s in line.split(' ') if s]
        self.name, self.address_type, self.service_type = sp[1:4]
        for i in range(index + 1, len(lines)):
            line = lines[i]
            if line.startswith('  ') or line.startswith('\t'):
                sp = [s.strip() for s in line.strip('\t').strip().split(' ') if s]
                prop = sp[0]
                value = sp[1] if len(sp) == 2 else None
                self.params[prop] = value
            else:
                return i
        return len(lines)


class IfaceParser(object):
    block_classes = (SourceBlock, SourceDirectoryBlock, AutoBlock, IfaceBlock)

    def __init__(self, config_file='/etc/network/interfaces'):
        self.config_file = config_file
        self.blocks = []
        lines = []
        if os.path.exists(config_file):
            with open(config_file) as f:
                lines = map(lambda s: s.strip('\n'), f.readlines())
        index = 0
        while index < len(lines):
            line = lines[index]
            keyword = line.split(' ', 1)[0]
            claz = self.get_class(keyword)
            inst = claz()
            self.blocks.append(inst)
            index = inst.process(lines, index)

    def get_class(self, keyword):
        for claz in self.block_classes:
            if claz.keyword == keyword:
                return claz
        return AnotherBlock

    def render(self):
        res = '\n'.join(map(lambda block: block.render(), self.blocks))
        return res

    def save(self):
        with open(self.config_file, 'w') as f:
            f.write(self.render())