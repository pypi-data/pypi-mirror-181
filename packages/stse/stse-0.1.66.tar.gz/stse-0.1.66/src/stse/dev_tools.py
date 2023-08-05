def json_to_py(path):
    with open(path) as f:
        data = f.read()
    data = data.replace('"', '\'').replace('true', 'True').replace('false', 'False').replace('null', 'None')
    return data