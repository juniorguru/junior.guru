def repr_item(item, fields):
    name = f"{item.__class__.__module__}.{item.__class__.__qualname__}"
    separator = ',\n    '
    data = [f"{field}={item[field]!r}"
            for field in fields
            if field in item]
    if len(fields) < len(item):
        data.append(f'[{len(item)} fields in total]')
    return f"{name}(\n    {separator.join(data)}\n)"
