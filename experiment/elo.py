class One(object):

    def me(self, arg):
        print('One', arg)


class Two(One):

    def me(self):
        print("Two")
        super().me('2')


class Three(One):

    def me(self):
        print("Three")
        super().me('3')


class Four(Two, Three):

    def me(self):
        print("Four")
        super().me('4')


Four().me()
