python3.10 -m venv venv

source venv/bin/activate

pip install requests


------

sudo docker build -t fastapi-upload-app .

sudo docker run -p 8000:8000 fastapi-upload-app
-----
test with ipynb

--------
Useful info

sudo docker run -d --name fastapi-app -p 8000:8000 fastapi-upload-app    # this starts the image running the container has name fastapi-app and is detached from the terminal

sudo docker exec -it fastapi-app /bin/bash    # this open in cli a bash with the structure inside the image folder

 sudo docker exec fastapi-app sh -c "rm -f /app/uploads/*"   #this deletes every previous file inside the uploads folder

 curl -X POST http://127.0.0.1:8000/upload -F "files=@test.txt" -F "files=@test1.txt" -F "files=@/home/kpanag/Downloads/t.txt"    # this uploads the files inside the container and uploads directory

 curl -X GET http://127.0.0.1:8000/getResults  # this runs relik on each uploaded file

 curl -X GET http://127.0.0.1:8000/getAllRelationTypes   #this returns all available relations not implemented yet

 curl -X GET http://127.0.0.1:8000/getAllEntityTypes   #this return all entity types not implemented yet 
