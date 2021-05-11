# Python POST script in Flask
Simple python script running in Docker with Nginx as proxy, based on Flask framework accepting POST requests and writing them to Postgressql database

### Prerequisities
All you need for running an application are:
 * Linux
 * Docker
 * Docker-compose

### Usage
All components (Flask, Nginx, Postgressql) are wrapped up as a Docker containers with docker-compose for quick instantiation. To run application do following:

Clone repository to your local machine (script was tested on Ubuntu 20.04):
```
git clone https://github.com/michalgozdowski/python_post_sentione.git
```
Run docker-compose command inside python_post_sentione directory:
```
docker-compose up -d
```
Application is running on localhost, port 8080, allowing requests to /store.  

### Test application
Nginx is setup to allow only POST requests, so application is working as a write-only script accepting JSON data in following format:
```
{
  "name": ...,
  "category": ...,
  "price": ...
}
```
To test if the application is accepting POST requests run:
```
curl -X POST -H "Content-type: application/json" -d '{"name": "", "category": "", "price": }' '127.0.0.1:8080/store'
```
E.g.:
```
curl -X POST -H "Content-type: application/json" -d '{"name": "Nissan Datsun 280Z", "category": "Cars", "price": 100000 }' '127.0.0.1:8080/store'
```
Application is allowing only POST requests, so when GET you will see:
```
curl 127.0.0.1:8080/store
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.19.10</center>
</body>
</html>
```

### GET, PUT, DELETE
Nginx is setup to deny GET, PUT and DELETE requests. To test if the data is properly written to database, remove following line from the nginx/nginx.conf:
```
limit_except POST {deny all;}
```
And run docker-compose again to apply change:
```
docker-compose up --build -d 
```

Then to GET all products run:
```
curl 127.0.0.1:8080/store
```

Or for one product only:
```
curl 127.0.0.1:8080/store/<name>
```

With nginx config changed, script is accepting PUT and DELETE requests as well. 
