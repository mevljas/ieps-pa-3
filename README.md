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

## SSL Certificate Exception When Downloading NLTK Data (MacOS)
If you get an SSL exception when downloading NLTK data, you can try to download the data manually from by running the following in the command line. A window will pop up, where you can select the data you want to download, in this case `punkt` and `stopwords`.

The solution is from https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087.
```bash
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
```