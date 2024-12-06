from api.logic.dynamic_media import ENTRY_RESOLVERS, register_entry_resolver

def test_register_entry_resolver():
    assert ENTRY_RESOLVERS == {}

    def resolver():
        pass

    register_entry_resolver("kind", resolver)

    assert ENTRY_RESOLVERS == {"kind": resolver}
