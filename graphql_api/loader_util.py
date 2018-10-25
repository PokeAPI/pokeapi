from .loader_key import LoaderKey

#####################################
# Some utility functions for loaders.
#####################################


def unbatch(keys, values, id_attr):
    """
    Unbatch a results list. Given a list of `keys` and a list of `values`, return a list of values with the same length and order as `keys`, where each value is selected based on its `id_attr` attribute.

    Example:
    ```
    values = [
        SomeObject(id=1, val="x"),
        SomeObject(id=2, val="x"),
        SomeObject(id=3, val="y"),
    ]
    unbatch([1, 2, 1], values, "id")
    ```

    Output:
    ```
    [
        SomeObject(id=1, val="x"),
        SomeObject(id=2, val="x"),
        SomeObject(id=1, val="x"),
    ]
    ```
    """

    results = []
    for key in keys:
        value = None
        for obj in values:
            if str(getattr(obj, id_attr)) == str(key):
                value = obj
                break
        results.append(value)
    return results


def create_batches(keys):
    """
    Batch a requests list. Given a list of `keys` (instances of LoaderKey), return a dictionary that groups each key's `id` value under its `args` value in a dictionary. Each unique `args` object from `keys` forms the dictionary's keys while the dict's values are a list of corresponding key `id`s for values.

    Example input:
    ```
    [
        LoaderKey(id=1, arg1='x'),
        LoaderKey(id=2, arg1='x'),
        LoaderKey(id=3, arg1='z'),
        LoaderKey(id=1, arg1='z')
    ]
    ```

    Output:
    ```
    {
        Args(arg1='x',): [1, 2],
        Args(arg1='z',): [3, 1]
    }
    ```
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


def add_filters(query_set, args, **filter_map):
    """Return query_set with applicable filters applied.
     - query_set: Django query set
     - args: a dictionary containing filter values
     - filter_map: keyword arguments mapping the filter name to the ORM filter name
    """

    for sql_name, name in filter_map.items():
        if name in args and args[name] is not None:
            query_set = query_set.filter(**{sql_name: args[name]})
    return query_set
