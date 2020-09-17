from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def strip_params(url, param_names):
    parts = urlparse(url)
    params = {name: value for name, value
              in parse_qs(parts.query).items()
              if name not in param_names}
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))


def set_params(url, params):
    parts = urlparse(url)
    url_params = {name: value for name, value
                  in parse_qs(parts.query).items()}
    for name, value in params.items():
        url_params[name] = ['' if value is None else str(value)]
    query = urlencode(url_params, doseq=True)
    return urlunparse(parts._replace(query=query))


def increment_param(url, param_name, inc=1):
    parts = urlparse(url)
    params = parse_qs(parts.query)
    params.setdefault(param_name, ['0'])
    params[param_name] = str(int(params[param_name][0]) + inc)
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))
