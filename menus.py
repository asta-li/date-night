"""
Pulls menu data from OpenTable links.
"""

import argparse
import collections
import csv
import datetime
import logging
import os
import sys
import time
import traceback
import urllib.request
import json

from lxml import html
import requests


logger = logging.getLogger(__name__)


Restaurant = collections.namedtuple(
    "Restaurant", "name link rating num_reviews price cuisine district num_bookings")


def find_in_tree(root, class_name="_1G0wk7EM8pIpucVz0MX3oo"):
    if "class" in root.keys():
        print(root.get("class"))
    if "class" in root.keys() and root.get("class") == class_name:
        return root
    for child in root:
        result = find_in_tree(child, class_name)
        if result is not None:
            return result
    return None


def find_keyword_node(root, keyword="menu"):
    visited = set(root)
    queue = [root]
    keyword_found = False
    keyword_nodes = []
    while queue:
        curr_node = queue.pop(0)
        if any(keyword in value for value in curr_node.values()):
            keyword_found = True
            keyword_nodes.append(curr_node)
        if keyword_found:
            continue
        for child_node in curr_node:
            if child_node in visited:
                continue
            visited.add(child_node)
            queue.append(child_node)
    if len(keyword_nodes) > 1:
        return keyword_nodes[0].getparent()
    if len(keyword_nodes) == 1:
        return keyword_nodes[0]
    return None


def parse_menu(url):
    # response = urllib.request.urlopen(url)
    # web_content = response.read()

    # Find the node containing the menu.
    find_keyword_node(tree)

    page = requests.get(url)
    tree = html.fromstring(page.content)
    for child in tree:
        if child.tag == "body":
            print(child)
            break


    import IPython; IPython.embed(); quit()


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--data", default="data_filtered.csv",
        help="Path to file containing cleaned restaurant data, including OpenTable links.")
    args = parser.parse_args()

    menus = {}
    with open(args.data, 'r') as f:
        for name, link, _, _, _, _, _, _ in csv.reader(f):
            if name == "name":
                continue
            menus[name] = parse_menu(link)
            
    with open("menus.json", "w") as f:
        json.dump(menus, f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
