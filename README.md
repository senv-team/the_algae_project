# Algae Project

This project is structured into several parts, each with its own specific role:

- **Datasets**: All data should be stored in the `datasets` directory. This data will not be pushed to GitHub as it is part of the `.gitignore` file. Everyone should have this data locally.

- **Data Access**: This part contains the code for accessing the data. It is a code-only section.

- **Data Exploration**: This part includes the code for exploratory data analysis. It can include tasks such as plotting data, looking for missing data, etc. This is also a code-only section.

- **Data Processing**: This part contains the code for the actual data processing. It is a code-only section.

- **Results**: All result directories should have the prefix "tmp". For example: "tmp_results_sentinel_v2".

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
