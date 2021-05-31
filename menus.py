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
import json

from lxml import html
import requests


logger = logging.getLogger(__name__)


Restaurant = collections.namedtuple(
    "Restaurant", "name link rating num_reviews price cuisine district num_bookings")


def find_in_tree(root, key, value):
    """Returns a node in the tree with the matching value for the given key."""
    if key in root.keys() and root.get(key) == value:
        return root
    for child in root:
        result = find_in_tree(child, key, value)
        if result is not None:
            return result
    return None


def find_keyword_node(root, keyword):
    """Find the first node in the tree containing the given keyword.
    
    If multiple child nodes at the same level satisfy the criteria, return the parent node.
    """
    visited = set([root])
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


def collect_values(root, key):
    """Collect all the values in the tree corresponding to the given key."""
    values = []
    if key in root.keys():
        values.append(root.get(key))
    for child in root:
        values.extend(collect_values(child, key))
    return values


def collect_text(root):
    """Collect all the text in the tree as a list."""
    text = []
    if root.tag != "script" and root.tag != "style" and root.text:
        text.append(root.text)
    for child in root:
        text.extend(collect_text(child))
    return text


def parse_menu(url):
    """Parse the on-page menu given the OpenTable URL."""
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Navigate into the html body.
    for body in tree:
        if body.tag == "body":
            break

    # Find the first node within the body containing information about the menu.
    menu_root = find_keyword_node(body, "oc-menu")
    if menu_root is None:
        menu_root = find_keyword_node(body, "menu-")
    menu_content = collect_text(menu_root)
    return menu_content


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
            logger.info("Processing: {}".format(name))
            menu_text = parse_menu(link)
            if len(menu_text) < 5:
                continue
            menus[name] = menu_text

            # Dump data every once in a while as we go.
            if len(menus) % 10 == 0:
                with open("menus.json", "w") as f:
                    json.dump(menus, f)
            
    with open("menus.json", "w") as f:
        json.dump(menus, f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
