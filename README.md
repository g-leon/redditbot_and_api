# redditbot_and_api
A small system that parses live data, stores it in a database and exposes it with filtering capabilities through an HTTP API. The ingested data will consist of reddit submissions/comments.

Mainly the program monitors a set of subreddits and extracts the newest submissions and comments. Data is fetched periodically through reddit’s API, normalized and stored in MongoDB in a standard format.

The system has three parts: a running MongoDB database, a long running Python that periodically queries for new submissions/comments in the targeted subreddits, grabs them, formats them and writes them to mongo and a web server that exposes an http endpoint: `/items?subreddit=<subreddit>&from=<t1>&to=<t2>`

The system can be run as a whole through docker-compose or by starting each individual component.

### Run dockerized system
    - cd dockerized_redditbot_and_api
    - docker-compose up --build
    
### Query system

    - http://localhost:5000/items?subreddit=python&from=1386915880&to=1486915880
 

