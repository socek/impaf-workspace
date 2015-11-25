class First(object):

    class Meta(object):
        z = 10


class Second(First):

    class Meta(First.Meta):
        z = 15

print(Second().Meta.z)
