class CachedRegistry:
    def __init__(self):
        self._cached_items = {}
        self._factories = {}

    def register(self, name, cls=None):
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

    def unregister(self, name):
        if name in self._factories:
            del self._factories[name]

    def get(self, name: str, *args, **kwargs):
        if name not in self._cached_items:
            self._cached_items[name] = self._factories.get(name)(*args, **kwargs)

        return self._cached_items[name]
