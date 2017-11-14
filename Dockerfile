FROM fedora:25

RUN yum install -y python python-devel boost-devel autoconf gcc-c++ \
  openssl-devel libxml2-devel libcurl-devel


# Set the WORKDIR to /app so all following commands run in /app
WORKDIR /app

# Install pythoncm
COPY vendor/pythoncm-8.0-127839_3a2d8e50cd ./pythoncm
RUN cd pythoncm && ./build.sh && make install

ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/lib

# Install requirements
COPY requirements.txt dev-requirements.txt ./
RUN pip install -r requirements.txt -r dev-requirements.txt

# Copy app
COPY . ./

