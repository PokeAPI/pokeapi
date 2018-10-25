from ..loader_key import LoaderKey

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
