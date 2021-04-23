# NHL Award Prediction Tracker
### Using Vue.js and FastAPI

Currently actively deployed.  Visit at http://www.nhlawardpredictions.com.

This is a maching learning-backed application geared towards predicting end-of-season voting outcomes for the National Hockey League's individual player awards/trophies.  It was written using Python 3.7.3 and NodeJS 4.16.1.  The application backend/API uses [FastAPI](https://fastapi.tiangolo.com/) and runs on a Uvicorn ASGI server.  The application frontend/UI is built using [Vue.js (version 3)](https://v3.vuejs.org/) as well as [Material Design Bootstrap 5](https://mdbootstrap.com/) as the foundation for styling.

Web scraping is done using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/); API requests made using Python's requests module.  Data aggregation & preprocessing + modeling is done using numpy, pandas, and scikit-learn.  See [this Jupyter notebook file](https://nbviewer.jupyter.org/github/jfbriggs/nhl_norris_voting/blob/master/NorrisTrophyVoting.ipynb) for the original machine learning project that serves as this application's foundation.

Deployment using Docker uses Node + NGINX images as the foundation for the frontend container, and a Gunicorn + Uvicorn + FastAPI image as the foundation for the backend container.
