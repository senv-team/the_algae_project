# How to save files:

* name_of_what_you_save_data.csv
* in directory: the_algae_project/datasets/csv
* example: the_algae_project/datasets/csv/ONI_data.csv
* example: the_algae_project/datasets/csv/cherry_blossom_data.csv

# What to write into a file

* Year, then either months, or months averages
* Make sure to only ever save one information in each csv file
* Years 1950-2025 (aka next year, which is obv not available yet ...) hence, for now 2024

for every month (e.g. temperature, sun activity) - can also be jan, feb, ... instead of 3 months mean

| year | DJF  | JFM  | FMA  | MAM  | AMJ  | MJJ  | JJA  | JAS  | ASO  | SON  | OND  | NDJ  |
|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 1950 | -1.5 | -1.3 | -1.2 | -1.2 | -1.1 | -0.9 | -0.5 | -0.4 | -0.4 | -0.4 | -0.6 | -0.8 |
| 1951 | -0.8 | -0.5 | -0.2 | 0.2  | 0.4  | 0.6  | 0.7  | 0.9  | 1.0  | 1.2  | 1.0  | 0.8  |
| 2023 | -0.7 | -0.4 | -0.1 | 0.2  | 0.5  | 0.8  | 1.1  | 1.3  | 1.6  | 1.8  | 1.9  | 2.0  |

OR

for day of year (doy) aka once a year (e.g. last day of frost, first day/peak day of blossom)

| year | name_doy |
|------|----------|
| 1953 | 150      |
| 1954 | 147      |

OR

something that is countable in each year (e.g. bee death, glacier loss, ...)

| year | bee_death |
|------|-----------|
| 1953 | 0         |
| 1954 | 0         |
