"""
Cleans up raw restaurant data scraped using https://dataminer.io/ from 
https://www.opentable.com/nearby/restaurants-near-me-san-francisco
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

logger = logging.getLogger(__name__)


Restaurant = collections.namedtuple(
    "Restaurant", "name link rating num_reviews price cuisine district num_bookings")


def process_data_format_1(input_file, data):
    with open(input_file, 'r') as f:
        for row in csv.reader(f):
            name, link, rating, num_reviews, price, details, num_bookings, _ = row

            # Skip the first line.
            if not link or link == "link":
                continue

            try:
                # Clean up column data.
                name = name.split(". ")[1].strip().strip("\"") if ". " in name else name
                link, _ = link.split("?")
                rating = float(rating[-9:-6]) if "0 stars" not in rating else 0.0
                num_reviews = int(num_reviews.strip("()"))
                price = price.split("<span")[0].strip("\"")
                _, cuisine, district = details.split("• ")
                cuisine = cuisine.strip()
                num_bookings = int(num_bookings.split("Booked ")[1].split(" time")[0]) if "Booked" in num_bookings else 0
            except Exception as err:
                print(traceback.print_exc())
                import IPython; IPython.embed(); quit()
                
            if rating == 0.0 or num_reviews == 0:
                continue

            # Put data into dictionary.
            data[name] = Restaurant(name, link, rating, num_reviews, price, cuisine, district, num_bookings)


def process_data_format_2(input_file, data):
    with open(input_file, 'r') as f:
        for row in csv.reader(f):
            name, link, rating, num_reviews, price, cuisine, district, num_bookings = row

            # Skip the first line.
            if not link or link == "link":
                continue

            try:
                # Clean up column data.
                link, _ = link.split("?")
                rating = float(rating.split(" stars out of 5")[0].split("aria-label=\"")[1]) if " stars out of 5" in rating else 0.0
                num_reviews = int(num_reviews.strip("()")) if num_reviews else 0
                price = price.replace(" ", "")
                num_bookings = int(num_bookings.split("Booked ")[1].split(" time")[0]) if "Booked" in num_bookings else 0
            except Exception as err:
                print(traceback.print_exc())
                import IPython; IPython.embed(); quit()

            # Put data into dictionary.
            data[name] = Restaurant(name, link, rating, num_reviews, price, cuisine, district, num_bookings)



def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--data_format_1", default="raw_data_1.csv",
        help="Path to file containing raw restaurant data.")
    parser.add_argument(
        "--data_format_2", default="raw_data_2.csv",
        help="Path to file containing raw restaurant data.")
    args = parser.parse_args()

    data = {}
    process_data_format_1(args.data_format_1, data)
    process_data_format_2(args.data_format_2, data)

    # Write to output file.
    with open("data.csv", 'w') as f:
        f.write("name, link, rating, num_reviews, price, cuisine, district, num_bookings\n")
        for item in data.values():
            if item.rating == 0.0 or item.num_reviews == 0:
                continue
            if "test" in item.name or "Test" in item.name or not item.link:
                continue
            f.write(", ".join(str(x) for x in item._asdict().values()) + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
