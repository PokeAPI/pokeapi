from ..loader_key import LoaderKey


def create_batches(keys):
    """
    Batch a requests list. Given a list of `keys` (instances of LoaderKey), return a dictionary that groups each key's `id` value under its `args` value in a dictionary. Each unique `args` object from `keys` forms the dictionary's keys while the dict's values are a list of corresponding key `id`s for values.
    """

    batches = {}
    for key in keys:
        assert isinstance(key, LoaderKey), (
            "The 'create_batches' function requires keys of type %s, not %s"
            % (LoaderKey, type(key))
        )
        if key.args in batches:
            batches[key.args].append(key.id)
        else:
            batches[key.args] = [key.id]

    return batches


def batch_fetch(keys, get_query_set_fn, id_attr):
    """
    Fetch multiple lists of values in batches. Given a list of `keys` (instances of LoaderKey), return a list of results the same length as `keys`, with each result corresponding to the correct key. Each result is a list of values that match up to the key.

    The values are batch-fetched with the provided `get_query_set_fn(ids, **args)`, and each value is matched up to the key by comparing the `id_attr` of the value to the key's id.
    """

    # Create a new query set for each set of args using `get_query_set_fn`
    batched_items = {}
    for args, ids in create_batches(keys).items():
        # Should ids be de-duplicated?
        batched_items[args] = get_query_set_fn(ids, **args._asdict())

    # Iterate through each item in each batch and match it to the keys
    # to create a results list
    results = []
    for key in keys:
        values = []
        for args, batch in batched_items.items():

            # Don't bother going down the rabbit hole if this one doesn't have
            # the right `args`
            if key.args == args:
                for item in batch:
                    if not hasattr(item, id_attr):
                        raise ValueError("%s has no id_attr %s" % (item, id_attr))

                    # Does it match?
                    if key.id == getattr(item, id_attr):
                        values.append(item)

        results.append(values)

    return results
