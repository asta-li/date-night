"""
Vectorize menu data.
"""

import argparse
import csv
import logging
import os
import sys
import json

import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


def preprocess_inputs(data_file, menus_file):
    """Collect data into a feature matrix."""
    NUM_MENU_FEATURES = 768
    NUM_REST_FEATURES = 6

    # Load menu data.
    with open(menus_file, 'r') as f:
        menus = json.load(f)

    # Create cuisine and district labels.
    cuisine_label = {}
    district_label = {}
    with open(data_file, 'r') as f:
        for _, _, _, _, _, cuisine, district, _ in csv.reader(f):
            if cuisine not in cuisine_label:
                cuisine_label[cuisine] = len(cuisine_label)
            if district not in district_label:
                district_label[district] = len(district_label)

    # Build up features.
    features = np.zeros([len(menus), NUM_MENU_FEATURES + NUM_REST_FEATURES])
    names = []

    with open(data_file, 'r') as f:
        for name, _, rating, num_reviews, price, cuisine, district, num_bookings in csv.reader(f):
            if name not in menus:
                continue
            # Fill restaurant features.
            i = len(names)
            features[i, 0] = float(rating)
            features[i, 1] = int(num_reviews)
            features[i, 2] = len(price)
            features[i, 3] = cuisine_label[cuisine]
            features[i, 4] = district_label[district]
            features[i, 5] = int(num_bookings)
            features[i, 6:] = menus[name]
            # Clean up and collect name.
            name = name.replace(" - SF", "").replace(" - San Francisco", "")
            names.append(name)

    return names, features


def plot_restaurants(X, names):
    """Visualize restaurant features in 2D using PCA."""
    # Dimensionality reduction to 2D.
    pca = PCA(n_components=2)
    projected_X = pca.fit_transform(X)

    fig,ax = plt.subplots()
    scatter_plot = plt.scatter(projected_X[:, 0], projected_X[:, 1])
    
    annotation = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annotation.set_visible(False)

    def update_annotation(indices):
        pos = scatter_plot.get_offsets()[indices[0]]
        annotation.xy = pos
        text = "\n".join(["{}: {}".format(i, names[i]) for i in indices])
        annotation.set_text(text)
        annotation.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        if event.inaxes != ax:
            return
        contains_mouse, ind = scatter_plot.contains(event)
        if contains_mouse:
            update_annotation(ind["ind"])
            annotation.set_visible(True)
            fig.canvas.draw_idle()
        elif annotation.get_visible():
            annotation.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()


def model(names, X, positive_names):
    """Learn restaurant recommendations given the input data.

    Requires names and features such that the ith name corresponds to the ith feature.
    """
    # Create 1.0 labels for positives and 0.0 labels for unknown examples.
    y = np.zeros([X.shape[0]])
    for i, name in enumerate(names):
        if name in positive_names:
            y[i] = 1.0

    # Normalize input features.
    # https://neerajkumar.org/writings/svm/#
    # Soft normalization: subtract the mean of the values and divides by (2 * standard deviation) 
    X = 0.5 * (X - np.mean(X, axis=0)) / np.std(X, axis=0)
    
    # Use biased SVM to solve the positive-unlabeled learning problem:
    # https://www.cs.uic.edu/~liub/publications/ICDM-03.pdf 
    # TODO: This is overfitting to the data.
    # clf = svm.SVC(kernel='linear', class_weight={1: 100})
    clf = svm.SVC(kernel='rbf', class_weight={1: 100})
    clf.fit(X, y)

    pred_y = clf.predict(X)
    for i, label in enumerate(pred_y):
        if label == 1.0:
            print("Index: {}, Restaurant: {}".format(i, names[i]))

    pred_scores = clf.decision_function(X)
    idx = np.argsort(-pred_scores)
    print("PREDICTIONS ON POSITIVES:")
    for i, label in enumerate(y):
        if label == 1.0:
            print(" * {}: {:.3f}".format(names[i], pred_scores[i]))
    print("MOST RECOMMENDED:")
    for i in idx[:20]:
        if names[i] not in positive_names:
            print(" * {}: {:.3f}".format(names[i], pred_scores[i]))
    print("LEAST RECOMMENDED:")
    for i in idx[-10:]:
        print(" * {}: {:.3f}".format(names[i], pred_scores[i]))
    
    plot_restaurants(X, names)

    # import IPython; IPython.embed()


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--data", default="data_filtered.csv",
        help="Path to file containing restaurant data.")
    parser.add_argument(
        "--menus", default="vectorized_menus.json",
        help="Path to file containing vectorized restaurant menu data.")

    args = parser.parse_args()

    positive_names = set([
        "Doppio Zero",
        "Maruya",
        "Gyu-Kaku",
        "Starbelly",
        "Trestle",
        "Marlowe",
        "Kokkari Estiatorio",
        "Nopa",
        "Spruce",
        "Zuni Cafe",
        "Mathilde French Bistro",
    ])

    names, features = preprocess_inputs(args.data, args.menus)
    model(names, features, positive_names)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
