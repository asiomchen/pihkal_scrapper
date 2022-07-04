# Pihkal Scrapper
Synthesys web scrapper for erowid version of Pihkal by Alexander and Ann Shulgin
https://erowid.org/library/books_online/pihkal/pihkal.shtml

Based on BeautifulSoup library


# Enviroment 
 All dependencies can be installed with `pip install -r requirements.txt`

# Usage
```python pihkal_scrapper.py start_procedure end_procedure```
where `start_procedure` and `end_procedure` are the number of the first and last procedure to parse
If running without parameters, the script will parse all procedures