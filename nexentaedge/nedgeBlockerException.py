class NedgeBlockerException(Exception):
    def __init__(self, blockers):
        #list of the current blockers
        self.blockers = blockers
