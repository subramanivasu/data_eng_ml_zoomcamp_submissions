#Specify all he instructions and dependencies we want to run 

#Installs the specified python version
FROM python:3.9.10

#Installs the dependency
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

#Workdirectory inside the docker image is specified
WORKDIR /app

#The file to run is copied from the source to the desired destination
COPY ingest_data.py ingest_data.py

#Specifies a self-sufficient task for the container to run
ENTRYPOINT ["python","ingest_data.py"]
