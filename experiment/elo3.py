def wrap(something):
    return something + 1


class One(object):

    @wrap
    me = 10
