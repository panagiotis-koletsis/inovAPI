python3.10 -m venv venv

source venv/bin/activate
pip install requests


------

sudo docker build -t fastapi-upload-app .

sudo docker run -p 8000:8000 fastapi-upload-app
-----
test with ipynb
