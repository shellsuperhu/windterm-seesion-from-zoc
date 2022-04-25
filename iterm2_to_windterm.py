#!/usr/bin/python3

import re
import json
import uuid


def get_file_context():
    with open("Profiles.json", "r") as f:
        context_list = f.readlines()
        context = ''.join(map(str, context_list))
        return context


def get_hosts_profile(context):
    json_data = json.loads(context)
    return json_data.get("Profiles")


def print_windterm_json(context):
    hosts = []
    for host_dict in get_hosts_profile(context):
        session_group = ">".join(map(str, host_dict.get("Tags")))
        session_label = host_dict.get("Name")
        session_port = 22

        command = host_dict.get("Command")
        if not re.match('.*ssh.*', command):
            continue
        session_target = command.split("@")[1]

        session_uuid = str(uuid.uuid4())
        host = {
            # "session.autoLogin": config.get("HOST", "password"),
            "session.autoLogin": "",
            "session.group": session_group,
            "session.icon": "session::square-darkturquoise",
            "session.label": session_label,
            "session.port": session_port,
            "session.protocol": "SSH",
            "session.target": session_target,
            "session.uuid": session_uuid
        }
        hosts.append(host)
    print(json.dumps(hosts))


if __name__ == "__main__":
    context = get_file_context()
    print_windterm_json(context)
