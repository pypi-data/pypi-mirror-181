from . import tools, forward_sessions
from click.shell_completion import CompletionItem


def sc_schemas(ctx, param, incomplete):
    schemas = tools._settings.get('schemas')
    result = []

    for schema_name in schemas:
        if not schema_name.startswith(incomplete):
            continue

        schema = schemas.get(schema_name)
        item = CompletionItem(schema_name, help=f"{len(schema)} session(s) for {schema_name}")
        result.append(item)
    return result


def ac_schemas(incomplete):
    schemas = tools._settings.get('schemas')
    result = []

    for schema_name in schemas:
        if not schema_name.startswith(incomplete):
            continue

        schema = schemas.get(schema_name)
        item = (schema_name, f"{len(schema)} session(s) for {schema_name}")
        result.append(item)
    return result


def sc_active_schemas(ctx, param, incomplete):
    return forward_sessions.list_from_active('schema', incomplete)


def ac_active_schemas(incomplete):
    return forward_sessions.list_from_active('schema', incomplete)


def sc_active_remote_port(ctx, param, incomplete):
    return forward_sessions.list_from_active('remote_port')


def sc_active_hosts(ctx, param, incomplete):
    return forward_sessions.list_from_active('hostname')


def ac_hosts(incomplete):
    from sshconf import read_ssh_config
    from os.path import expanduser
    result = []
    c = read_ssh_config(expanduser("~/.ssh/config"))
    for host in c.hosts():
        if "*" not in host and host.startswith(incomplete):
            result.append(host)
    return result


def sc_hosts(ctx, param, incomplete):
    from sshconf import read_ssh_config
    from os.path import expanduser
    result = []
    c = read_ssh_config(expanduser("~/.ssh/config"))
    for host in c.hosts():
        if "*" not in host and host.startswith(incomplete):
            item = CompletionItem(host)
            result.append(item)
    return result
