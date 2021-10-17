from pantomath.registry import CachedRegistry


def test_register():
    class Dummy:
        pass

    def factory():
        return Dummy()

    registry = CachedRegistry()
    registry.register("dummy", factory)
    assert isinstance(registry.get("dummy"), Dummy)
