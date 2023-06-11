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

## notes
- The sql database is stored in the `marketplace/data` folder so that it can be 
persisted even if the docker container is removed.
- Currently, no authentication is implemented, so anyone can register a bot.
- Therefor it should not be publicly exposed to the internet.
Security measures will be implemented in the next version
