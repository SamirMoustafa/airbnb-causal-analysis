# Airbnb Causal Analysis

#### Usage


`
bash  run.sh
`

> This example will scrape and clean and plot `berlin` city
> To scrape any city you want you can use the following command

`
python3 run.py --country --country "canada" --location "on" --city "toronto" --date "2020-05-07"
`

#### Project tree:

```
.
├── assets
├── data
│   ├── berlin2020-05-14.csv
│   ├── london2020-04-14.csv
│   ├── national solution
│   │   ├── data_cleaned.csv
│   │   ├── data cleaning.ipynb
│   │   ├── data mining.ipynb
│   │   ├── data visualization.ipynb
│   │   └── dirty_data.csv
│   └── toronto2020-05-07.csv
├── LICENSE
├── project_reproducing
│   ├── dag_output.png
│   ├── first_project.ipynb
│   ├── second_project.ipynb
│   └── third_project
│       ├── Causal_Data_Science_Notebook.ipynb
│       ├── data
│       │   ├── listings.csv
│       │   ├── listings_full.csv
│       │   └── listings_manual.csv
│       ├── images
│       │   ├── airbnb_header.png
│       │   ├── dag1.png
│       │   ├── dag2.png
│       │   ├── redfinScrapping.gif
│       │   ├── walkScores.png
│       │   ├── Zillow_1.jpg
│       │   ├── Zillow_2.jpg
│       │   └── zillow_south_boston.png
│       ├── model_tests_notebook.ipynb
│       └── README.md
├── airbnb_dataset_links.csv
├── src
│   ├── causal
│   │   ├── __init__.py
│   │   └── models.py
│   ├── nlp
│   │   ├── __init__.py
│   │   └── tf_idf.py
│   ├── preprocessing
│   │   ├── clean.py
│   │   └── __init__.py
│   ├── scrape
│   │   ├── __init__.py
│   │   └── scraper.py
│   └── utils.py
├── README.md
├── run.py
└── run.sh

```