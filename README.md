# Date Night

This project makes restaurant reservations for my weekly date night.

## Setup

### Requirements / Initial setup
- Install miniconda: https://docs.conda.io/en/latest/miniconda.html
- Set up the conda and pip environments.
```
conda env create -f environment.yml
pip install requirements.txt
```

Download Chromedriver and add to your PATH: https://chromedriver.chromium.org/downloads

### Enter the conda environment
```
conda activate date
```
To exit, run `conda deactivate`.

### Set up environment
Load the following variables into your environment:
```
OPENTABLE_EMAIL
OPENTABLE_PASSWORD
```
