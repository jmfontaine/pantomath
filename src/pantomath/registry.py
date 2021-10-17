"""A registry that lazily instantiates and caches objects"""


class CachedRegistry:
    """A registry that lazily instantiates and caches objects"""

    def __init__(self):
        """Constructor."""
        self._cached_items = {}
        self._factories = {}

    def register(self, name: str, cls=None):
        """Registers a factory for an object."""

        # Invoked as function
        if cls:
            cls.type = name
            self._factories[name] = cls
            return cls

        # Invoked as class decorator
        def _register_class(cls):
            self._factories[name] = cls
            cls.type = name
            return cls

        return _register_class

    def unregister(self, name: str) -> None:
        """Unregisters a factory for an object."""

        if name in self._factories:
            del self._factories[name]

    def get(self, name: str, *args, **kwargs):
        """Returns a object from the registry cache.

        The object will be instanciated and cached, if it is not in the cache already.
        """

        if name not in self._cached_items:
            self._cached_items[name] = self._factories.get(name)(*args, **kwargs)

        return self._cached_items[name]
