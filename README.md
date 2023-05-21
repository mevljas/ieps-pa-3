# WIER (IEPS) Programming Assignment 3
Third programming assignment for the WIER (IEPS) faculty course. 
The main goal was to build a simple index and implement querying against it

## Project setup


### Install requirements

```bash
pip install -r requirements.txt
python -m nltk.downloader punkt, stopwords
```

## Running the project
1. Navigate to the `implementation-indexing` directory
2. Create an inverse index with `python create-index.py`
3. Run the algorithms:
- run **basic** search with `python run-basic-search.py` or
- run **SQLite** search with `python run-sqlite-search.py`