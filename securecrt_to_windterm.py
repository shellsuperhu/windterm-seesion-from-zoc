#!/usr/bin/python3

import re
import json
import uuid
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def get_sessions_child_nodes_elements():
    child_nodes_elements = []
    doc = minidom.parse('crt.xml')

    elements = doc.getElementsByTagName('key')
    sessions_element = {}
    for e in elements:
        if e.getAttribute("name") == "Sessions":
            sessions_element = e
            break
    for e in sessions_element.childNodes:
        if e.nodeType != e.TEXT_NODE:
            child_nodes_elements.append(e)
    return child_nodes_elements


def recursion_get_child_nodes_by_element(element, hosts_dict, tree_dict):
    child_elemets = []
    for node in element.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.tagName == "key":
            child_elemets.append(node)

    cut_label = element.getAttribute("name")
    if len(child_elemets) == 0:
        host_label = cut_label
        session_uuid = str(uuid.uuid4())

        session_target = ""
        session_port = ""
        for e in element.getElementsByTagName("dword"):
            if e.getAttribute("name") == "[SSH2] Port":
                session_port = int(e.firstChild.nodeValue)
                break

        for e in element.getElementsByTagName("string"):
            if e.getAttribute("name") == "Hostname":
                session_target = e.firstChild.nodeValue
                break

        host_dict = {
            "session.autoLogin": "",
            "session.icon": "session::square-darkturquoise",
            "session.label": host_label,
            "session.port": session_port,
            "session.protocol": "SSH",
            "session.target": session_target,
            "session.uuid": session_uuid
        }
        hosts_dict[host_label] = host_dict
    else:
        for child_element in child_elemets:
            parent_label = cut_label
            child_label = child_element.getAttribute("name")
            t_dict = {
                "parent_name": parent_label,
                "name": child_label
            }
            tree_dict[child_label] = t_dict
            recursion_get_child_nodes_by_element(child_element, hosts_dict, tree_dict)


def recursion_get_full_paths_folder(parent_name, folders_tmp_dict, full_paths_folder):
    folders_tmp = folders_tmp_dict.get(parent_name)
    parent_name = folders_tmp.get("parent_name")
    name = folders_tmp.get("name")
    if parent_name == '0':
        full_paths_folder.insert(0, name)
        return full_paths_folder
    else:
        full_paths_folder.insert(0, name)
        recursion_get_full_paths_folder(parent_name, folders_tmp_dict, full_paths_folder)


def print_windterm_json():
    child_nodes_elements = get_sessions_child_nodes_elements()

    hosts = []
    for child_node_element in child_nodes_elements:
        child_label = child_node_element.getAttribute("name")
        child_nodes_dict = {}
        hosts_dict = {}
        tree_dict = {}
        tree_dict[child_label] = {
            "parent_name": "0",
            "name": child_label
        }
        recursion_get_child_nodes_by_element(child_node_element, hosts_dict, tree_dict)

        for session_label, session in hosts_dict.items():
            full_paths_folder = []
            recursion_get_full_paths_folder(session_label, tree_dict, full_paths_folder)

            session_group = ">".join(map(str, full_paths_folder))
            session["session.group"] = session_group
            hosts.append(session)

        # print(json.dumps(hosts_dict))
        # print(json.dumps(tree_dict))
        break
    print(json.dumps(hosts))


if __name__ == "__main__":
    print_windterm_json()
