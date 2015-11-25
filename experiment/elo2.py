class One(object):

    _data = {'one': 'one'}

    @property
    def data(self):
        old = dict(getattr(super(), 'data', {}))
        old.update(self._data)
        return old


class Two(One):

    _data = {'two': 'two'}

    # @property
    # def data(self):
    #     data = dict(super().data)
    #     data.update({'two': 'two'})
    #     return data


class Three(One):
    _data = {'three': 'three'}

    # @property
    # def data(self):
    #     data = dict(super().data)
    #     data.update({'three': 'three'})
    #     return data

    def me(self):
        print("Three")
        super().me('3')


class Four(Two, Three):
    _data = {'four': 'four'}

    # @property
    # def data(self):
    #     data = dict(super().data)
    #     data.update({'four': 'four'})
    #     return data

    def me(self):
        print("Four")
        super().me('4')


print(Four().data)
