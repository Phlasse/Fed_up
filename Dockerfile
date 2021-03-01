### FROM the base image we want to build
FROM python:3.8.6-buster

### COPY file needed for the Docker images
COPY app /app
COPY Fed_up /Fed_up
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py
COPY scripts /scripts
COPY tests /tests
COPY Makefile /Makefile

### RUN the directives to install the dependancies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN make install

### CMD apply the command that the container should run once it has started
CMD streamlit run app/pages/app.py 