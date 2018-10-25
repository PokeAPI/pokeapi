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
