# Wiwino Market analysis

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## 📒 Description

The company. _Wiwino_, is proudly active in the wine industry. They have been gathering data about wines from their users for years. They want to have a better understanding of the wine market by analyzing this data.

This project aims to provide a tool for deriving useful insights from the gathered data.

## 📋 Data

Wiwino data is contained in an [SQLite](https://www.sqlite.org/index.html) database. 

Below is the database diagram. The `yellow keys` symbol represents `PRIMARY KEYS` while the `blue keys` symbol represents `FOREIGN KEYS`. Each column is typed. 

![DB diagram](./assets/vivino_db_diagram_horizontal.png)


## 📦 Repo structure

```
.
├── db/
│ └── vivino.db
├── analysis/
│ ├── alice.ipynb
│ ├── geraldine.ipynb
│ └── sem.ipynb
├── assets/
│ ├── vivimo_db_diagram_horizontal.png
│ └── presentation.pdf
├── streamlit/
│ └── query.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 🛠️ The Tool

The tool created is a website using Streamlit on the front-end, with visualization using Plotly and Pandas. At the back-end are queries using SQL.


## 🎮 Usage

1. **Clone the repository**: 

    ```
    git clone https://github.com/Rumineko/wiwino-drunkrat
    ```

2. **Install dependencies**: 

    ```
    pip install -r requirements.txt
    ```

3. **Run the program**: 

    ```
    cd streamlit
    streamlit run query.py
    ```
## ⏱️ Timeline

The development of this project took 5 days for completion.

## 📌 Personal Situation

This project was completed as part of the AI Boocamp at BeCode.org by team Drunkrat. 

Connect with the team on LinkedIn:
- [Alice Mendes](https://www.linkedin.com/in/alice-edcm/)
- [Geraldine Nadela](https://www.linkedin.com/in/gnadela/)
- [Sem Deleersnijder](https://www.linkedin.com/in/sem-deleersnijder-62b3bb286/)