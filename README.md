# simple-search-engine

this is one of my college projects from information retrieval coursework. What I built here is simple search engine that able to search from inverted index that built from news data that crawled from [detik](https://www.detik.com).

## Run the Web GUI
1. install the environment with command: <br>
`conda env create -f environment.yml --name some_env_name`
2. activate the virtual environment
3. change directory to /web_app
4. run the web server: <br> `uvicon main:app --reload`
5. go to 127.0.0.1/site

## Re Crawling Data and Build the Inverted Index
1. install and activate the enviroment, see the step from above steps
2. run crawling.py (this only crawl the news from the first page of indeks berita detik, modification if you want to get more data)
3. run inverted_index.py

