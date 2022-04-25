#!/usr/bin/python3

import re
from configparser import ConfigParser
import io
import json
import uuid

config = ConfigParser()


def get_file_context():
    with open("HostDirectory.zocini", "r") as f:
        context_list = f.readlines()
        context = ''.join(map(str, context_list))
        return context


def recursion_get_full_paths_folder(floder_parent_id, folders_tmp_dict, full_paths_folder):
    folders_tmp = folders_tmp_dict.get(floder_parent_id)
    floder_parent_id = folders_tmp.get("floder_parent_id")
    folder_name = folders_tmp.get("folder_name")
    if floder_parent_id == '0':
        full_paths_folder.insert(0, folder_name)
        return full_paths_folder
    else:
        full_paths_folder.insert(0, folder_name)
        recursion_get_full_paths_folder(floder_parent_id, folders_tmp_dict, full_paths_folder)


def get_folders(context):
    """
    folders_tmp_dict
    {
        folder_id: {
            floder_parent_id:
            folder_name:
        }
    }

    folders_dict
    {
        folder_id: [full_paths_folder]
    }
    :param context:
    :return:
    """
    folders_tmp_dict = {}
    folders_dict = {}
    match_list = re.findall(r'(\[STRUCTURE\]\n(.+?\n|^$\n)+?)\[/STRUCTURE\]\n', context, flags=re.MULTILINE)
    buf = io.StringIO(match_list[0][0])
    config.read_file(buf)
    for item in config.items("STRUCTURE"):
        if re.match(r'^folder.*', item[0]):
            folder_id = item[0].split("#")[1]
            floder_parent_id = item[1].split("|")[0].split(".")[1]
            folder_name = item[1].split("|")[1]

            folders_tmp_dict[folder_id] = {
                "floder_parent_id": floder_parent_id,
                "folder_name": folder_name
            }

    for folder_id, item_dict in folders_tmp_dict.items():
        full_paths_folder = []
        recursion_get_full_paths_folder(folder_id, folders_tmp_dict, full_paths_folder)
        folders_dict[folder_id] = full_paths_folder
    return folders_dict


def get_hosts_list(context):
    match_list = re.findall(r'(\[HOST\]\n(.+?\n)+?)\[/HOST\]\n', context, flags=re.MULTILINE)
    return match_list


def print_windterm_json(floder_dict, context):
    hosts = []
    for config_str_item in get_hosts_list(context):
        buf = io.StringIO(config_str_item[0])
        config.read_file(buf)

        folder_id = config.get("HOST", "folder")
        if folder_id == "0":
            continue

        session_group = ">".join(map(str, floder_dict.get(folder_id)))

        connectto_arr = config.get("HOST", "connectto").replace('"', '').split(":")
        session_target = connectto_arr[0]
        session_port = 22
        if len(connectto_arr) >= 2:
            session_port = int(connectto_arr[1])
        session_uuid = str(uuid.uuid4())
        host = {
            # "session.autoLogin": config.get("HOST", "password"),
            "session.autoLogin": "",
            "session.group": session_group,
            "session.icon": "session::square-darkturquoise",
            "session.label": config.get("HOST", "name").replace('"', ''),
            "session.port": session_port,
            "session.protocol": "SSH",
            "session.target": session_target,
            "session.uuid": session_uuid
        }
        hosts.append(host)
    print(json.dumps(hosts))


if __name__ == "__main__":
    context = get_file_context()
    floder_dict = get_folders(context)
    print_windterm_json(floder_dict, context)
