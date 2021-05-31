"""
Vectorize menu data.
"""


import argparse
import logging
import os
import sys
import json

import spacy


logger = logging.getLogger(__name__)


def vectorize(text_dict):
    """Convert text values in the dictionary into 768-dimensional vectors."""
    # nlp = spacy.load("en_core_web_md")
    nlp = spacy.load("en_core_web_trf") 

    # Vectorize the menu data.
    # for doc in nlp.pipe(text, disable=["tagger", "parser", "attribute_ruler"]):
    for i, (key, text) in enumerate(text_dict.items()):
        logger.info("Processing: {}".format(key))
        text = " ".join(text)
        doc = nlp(text)
        # TODO: weight token vectors with TF-IDF
        text_dict[key] = (doc._.trf_data.tensors[-1].mean(axis=0)).tolist()
        #import IPython;IPython.embed();quit()
        
        if i % 10 == 0:
            with open("vectorized_menus.json", "w") as f:
                json.dump(text_dict, f)

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--data", default="menus.json",
        help="Path to file containing restaurant menu data.")
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        menus = json.load(f)

    # Vectorize menu data.
    vectorize(menus)
            
    with open("vectorized_menus.json", "w") as f:
        json.dump(menus, f)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
