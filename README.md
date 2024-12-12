# Explore underlying factors of climate change

## Directory Structure
This project is structured into several parts, each with its own specific role:

- **Code for Mining**: This part contains the code for accessing, cleaning and converting the data to a csv file, stored in `datasets`. Code-only section.

- **Code for Processing**: This part contains the code for the actual data processing. Make sure not to access data outside the `datasets` directory. If you need additional data, it should be downloaded/cleaned/converted in the `data_mining` directory and saved in the `datasets` directory. Code-only section.

- **Code for Visualising**: This part contains the code for visualisations. The code should access result csv files from the `results` directory or `datasets` directory. Code-only section.

- **Datasets**: All data be stored in a sub-directory of `datasets`. Everyone should have this locally, `.gitignore` file handles this. No code here.
<<<<<<< HEAD

- **Locs**: All the geojson files of positions
=======
>>>>>>> cde1471d5ef5e779bba0eb937ddb0f6f26cba051

- **Results**: All results/plots should be stored in a sub-directory of `results`. Everyone should have this locally, `.gitignore` file handles this. No code here. 

Directories with prefix "tmp" will not be pushed to GitHub, see `.gitignore` file.

## Setting Up the Virtual Environment

To set up the virtual environment for this project, follow these steps:

1. Install `virtualenv`:

    ```shell
    pip install virtualenv
    ```

1. Create a virtual environment:

    ```shell
    virtualenv .venv
    ```

1. Activate the virtual environment:

    ```shell
    source .venv/bin/activate
    ```

1. Install the required packages:

    ```shell
    pip install -r requirements.txt
    ```
