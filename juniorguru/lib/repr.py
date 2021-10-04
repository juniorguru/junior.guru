def repr_item(item, fields):
    name = f"{item.__class__.__module__}.{item.__class__.__qualname__}"
    indent = (len(name) + 1) * ' '
    separator = f',\n{indent}'
    data = separator.join([f"{field}={item[field]!r}"
                           for field in fields
                           if field in item])
    if len(fields) < len(item):
        data += f'{separator}[{len(item)} fields in total]'
    return f"{name}({data})"
