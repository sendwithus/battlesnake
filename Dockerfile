FROM python:2.7.7

# Install requirements first, so we can skip unless the file changes
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy code to /src and run from there
ADD . /src
WORKDIR /src
