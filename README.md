# Movie_recommender
### A movie recommender pipeline hosted on a local flask server using non-negative matrix factorisation (NMF).
* NMF is trained with 100 latent components and saved as a pickle file for later reuse
* The data is linked to a local Postgres database and accessed every time the model is trained
* The user interface is coded in HTML and formatted in CSS with Bootstrap
<br/><br/>
### To do:
* Finish data processing module such that it appends each user data to the Postgres database
* Improve visual layout of HTML, incl. 5 star rating and improved Recommendation.html layout
* Package application in Docker, including connection to a Dockerized Postgres DB
