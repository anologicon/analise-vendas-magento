FROM python:3.8.0

# exposing default port for streamlit
EXPOSE 8501

# copy over and install packages
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copying everything over
COPY . .

# run app
CMD streamlit run webapp/App.py