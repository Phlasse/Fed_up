### FROM the base image we want to build
FROM python:3.8.6-buster

### COPY file needed for the Docker images
COPY app /app
COPY Fed_up /Fed_up
COPY requirements.txt /requirements.txt
COPY setup.sh /setup.sh
COPY setup.py /setup.py
COPY scripts /scripts
COPY tests /tests
COPY Makefile /Makefile

### EXPOSE Port 8080
EXPOSE 8080

### RUN the directives to install the dependancies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN make install

### CMD apply the command that the container should run once it has started
CMD sh setup.sh && streamlit run --server.port 8080 app/pages/app.py 