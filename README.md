# bike-streaming
The purpose of this project is to experiment with deploying machine learning models into a kafka environment and to perform real-time predictions.
The streaming data comes from NYC Bike stations and is consumed from https://www.satori.com/opendata/channels/NYC-Bike-Live-Station via a python aplication and is saved to a sqlite database. Furthermore, an easy to deploy infrastrcuture has been developed to deploy the  ingestion from satori, kafka, zookeeper and kafka-connect-jdbc-source with a docker-compose setup.
To be developed: mahout regression model which coefficients will be stored in kafka, kafka-streaming app which reads coefficients and runs machine learning model, spring microservice which makes predictions available per REST API.

# deployment
Prerequesites:
Add a config.yml file unser ingestion-to-db/src with following content (channel, endpoint and dbpath are optional - will only be used if you want to run the python script locally without docker:

```yaml
ingestor:
  apikey: 'xxx'
  channel: 'NYC-Bike-Live-Station'
  endpoint: 'wss://open-data.api.satori.com'
  dbpath: '/foo/bar'
 ```
Setup environment variables in docker/docker-compose.yml.

Run kafka-docker/docker-compose-up.sh
