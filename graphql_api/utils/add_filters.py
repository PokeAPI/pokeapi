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
