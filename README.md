# Audio API
A simple API server to handle user audio projects. 
Provides endpoints that allow a user to perform the following actions:

1. POST raw audio data and store it.\
Eg: $ curl -X POST --data-binary @myfile.wav http://localhost:5000/post?file=myfile.wav 

2. GET a list of stored files.\
Eg: $ curl http://localhost:5000/list?maxduration=300 

3. GET the contents of stored files.\
Eg: $ curl http://localhost:5000/download?name=myfile.wav

4. GET the metadata of stored files.\
Eg: $ curl http://localhost:5000/info?name=myfile.wav

## Usage
pip3 install -r requirements.txt \
python3 rest_api.py

