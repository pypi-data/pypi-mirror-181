class BaseUser:
    """Base user class."""

    first_name: str = ''
    last_name: str = ''
    email: str = ''
    username: str = ''

    def __iter__(self):
        """Provide dict representation of the class."""
        iters = {key: getattr(self, key) for key in self.__dir__() if key[:1] != '_'}
        iters.update(self.__dict__)

        for key, val_ in iters.items():
            yield key, val_

    def __str__(self):
        """Override default str."""
        return str(self.__class__) + '\n' + '\n'.join(
            ('{0} = {1}'.format(attr, self.__dict__[attr]) for attr in self.__dict__),
        )
