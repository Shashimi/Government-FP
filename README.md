Government-FP
=============

Hackbright Spring 2014 final project 

An app to generate a hierarchical, comprehensive list of all state and federal representatives for a given zip code, complete with social media links, general contact info, and all bills and votes involving each representative. 


Overview

Utilized data from 2 downloaded govtrack.us files, scraped information from official Nevada municipal websites, and used a govtrack.us API for Congressional information and bills. 
Parsed data from all 3 sources as JSON.
Stored all data in a PostgreSQL database; used SQLAlchemy to interact with DB
Three-page app built on Python/Flask and Bootstrap/HTML/CSS
Soon to be deployed through Heroku

Improvements / Future Features

Integrate an RSS feed of live voting data from popVox onto the front page
Scale data for western states
Create a better design for the hierarchical layout of representatives 
