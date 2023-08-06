import re
from sqlalchemy.engine.url import make_url

GROUP_DELIMITER = re.compile(r"\s*\,\s*")
KEY_VALUE_DELIMITER = re.compile(r"\s*\:\s*")


def parse_boolean(bool_string):
    bool_string = bool_string.lower()
    if bool_string == "true":
        return True
    elif bool_string == "false":
        return False
    else:
        raise ValueError()


def parse_url(origin_url):
    url = make_url(origin_url)
    query = dict(url.query)

    instance_name = url.host.split('.')[0]
    length = len(instance_name) + 1

    host = 'https://' + url.host[length:]
    workspace = url.database
    username = url.username
    driver_name = url.drivername
    pwd = url.password

    if 'virtualcluster' not in query:
        raise ValueError('url must have `virtualcluster` parameter.')
    else:
        vc_name = query.pop('virtualcluster')

    return (
        host,
        username,
        driver_name,
        pwd,
        instance_name,
        workspace,
        vc_name,
    )
