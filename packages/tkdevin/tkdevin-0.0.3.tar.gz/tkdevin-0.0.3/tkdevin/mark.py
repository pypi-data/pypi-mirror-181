def mark_init():
    if not is_mark_init():
        from os import mkdir
        mkdir(".//markdata")
        with open(".//markdata//data.json", "w+", encoding="utf-8") as _file0:
            from json import dumps
            _file0.write(
                dumps(
                    {
                    },
                    indent=4, ensure_ascii=False
                )
            )
            _file0.close()


def is_mark_init() -> bool:
    from os.path import exists
    return exists(".//markdata")


def mark_data_key(data_name, data_context):
    from json import loads, dumps
    mark_init()
    _file1 = open(".//markdata//data.json", "r", encoding="utf-8")
    old_data = loads(_file1.read())
    _file1.close()

    _file2 = open(".//markdata//data.json", "w", encoding="utf-8")
    new_data = old_data
    new_data[data_name] = data_context
    _file2.write(
        dumps(
            new_data,
            indent=4, ensure_ascii=False
        ),
    )
    _file2.close()


def get_mark_data() -> dict:
    from json import loads
    mark_init()
    _file3 = open(".//markdata//data.json", "r", encoding="utf-8")
    get_data = loads(_file3.read())
    _file3.close()
    return get_data


def get_mark_data_key(data_name):
    from json import loads
    mark_init()
    return get_mark_data()[data_name]


def is_mark_data_key(data_name) -> bool:
    return data_name in get_mark_data()

def clear_mark_data():
    open(".//markdata//data.json", "w", encoding="utf-8").write("{\n}")
