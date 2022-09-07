class Activity:

    #__slots__ = ['dur', 'res', 'pred'] #???

    def __init__(self, index, dur, res, succ, pred):
        self.index = index
        self.dur = dur
        self.res = res
        self.succ = succ
        self.pred = pred
