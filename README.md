This is for testing the notebooks in production phase 

python3.10 -m venv venv

source venv/bin/activate

pip install requests

------

sudo docker build -t fastapi-upload-app .

sudo docker run -p 8000:8000 fastapi-upload-app
-----
test with ipynb
--------
Useful info for saving .tar image file in googgle drive

sudo docker save -o ~/Downloads/fastapi-upload-app.tar fastapi-upload-app

chmod 777 fastapi-upload-app.tar 

rclone copy fastapi-upload-app.tar remote: -v


----- INOV setup with example on Linux based terminal
In this process docker and curl (on terminal) should be downloaded
Also in case of organazation restriction the computer that runs the dockerized API needs to have access to huggingface and be able to download RELIK model: https://huggingface.co/sapienzanlp/relik-relation-extraction-nyt-large  #do not download it the code does
It has been tested on .txt files (You can see the files inside the container by doing cat test.txt and cat test1.txt) after sudo docker exec -it fastapi-app /bin/bash

1) Download the image : https://drive.google.com/drive/folders/1TqqyAafeK5z5DvfzdZ1knizYshg8EZ8O

2) docker image load -i fastapi-upload-app.tar #run the image with docker (Be careful to add the corect path in this command)

3) sudo docker run -d --name fastapi-app -p 8000:8000 fastapi-upload-app    # this starts the image running the container has name fastapi-app and is detached from the terminal and maps the image port

4) sudo docker exec fastapi-app sh -c "rm -f /app/uploads/*"   #this deletes every previous file inside the uploads folder on the image

5) curl -X POST http://127.0.0.1:8000/upload -F "files=@test.txt" -F "files=@test1.txt" -F "files=@/home/kpanag/Downloads/t.txt"    # this uploads the files inside the container and uploads directory

6) curl -X GET http://127.0.0.1:8000/getResults  # this runs relik on each uploaded file

7) curl -X GET http://127.0.0.1:8000/getAllRelationTypes   #this returns all available relations not implemented yet

8) curl -X GET http://127.0.0.1:8000/getAllEntityTypes   #this return all entity types not implemented yet 




Additional info

sudo docker start fastapi-app # if already you have created the container just run it 

sudo docker stop fastapi-app # Stop the container

sudo docker exec -it fastapi-app /bin/bash    # this open in cli a bash with the structure inside the image folder (You are propably not going to need this command! it is to verify the files are uploaded correctly inside the containder and uploads folder)

For windows based terminal the only thing that changes is that sudo should be removed from all commands and curl should be replaced with curl.exe
