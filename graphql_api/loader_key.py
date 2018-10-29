from collections import namedtuple
# pylint: disable=redefined-builtin

class LoaderKey:
    """
	A hashable, immutable key identifier for use in dataloaders. To use, create a
    LoaderKey object from a unique `id` and any other optional named kwargs. The `id`
    can be accessed using the `id` attribute, and the arguments using the `args`
    attribute (e.g. `loader_key_obj.args.arg1`).
	"""

    def __init__(self, id, **args):
        self.id = id

        # Convert mutable list args to immutable tuples
        for key, arg in args.items():
            if isinstance(arg, list):
                args[key] = tuple(arg)

        Args = namedtuple("Args", args.keys())
        self.args = Args(**args)

    def __hash__(self):
        return hash((self.id, self.args))

    def __eq__(self, other):
        return (self.id, self.args) == (other.id, other.args)

    def __ne__(self, other):
        return not self == other
