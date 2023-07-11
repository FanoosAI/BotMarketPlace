# BotMarketPlace
A market place for approved bots 

## APIs: 
- GET /public-bots:  Get all bots  
- POST /register: Register new bot 


## How to deploy:
- Clone the repo
- `cd` into the repo
- Build the dockerfile by running `docker build -t bot_marketplace .`
- Run the docker image by running: 
``` 
 docker run --name marketplace -v $(pwd)/marketplace/data:/app/marketplace/data -p 8058:8058 bot_marketplace:latest
```
The server will be running on port 8058

<hr>

## Security measures
the /public-bots can be accessed without any authentication. However, /register must only be 
accessible to authorized clients. (like botfather)
So, API keys are used for /register API. store the API keys in `marketplace/data/api_keys.yaml` file (which is ignored in 
the git repo) in this format:
```yaml
username: API_KEY
'@botfather:parsi.ai': SECRET_API_KEY
```
This API_KEY must be provided in the header of the POST request with it's key being 'Authorization'.
<hr>

## notes
- The sql database is stored in the `marketplace/data` folder so that it can be 
persisted even if the docker container is removed.
- The `marketplace/data/api_keys.yaml` file must be provided manually when deploying the project.