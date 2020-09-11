FROM python:3.8.0-slim

# copy over and install packages
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# copying everything over
COPY . .

# run app
CMD streamlit run webapp/app.py --server.port $PORT