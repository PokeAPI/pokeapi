# Build the app on top of Ubuntu
from ubuntu

# Patch and Install Dependencies
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install git python-dev make python-pip libpq-dev

# Add the application code to the image
ADD . /root/

# Set a working directory
WORKDIR /root/

# Build the application
RUN make install
RUN make setup

# Build the v2 database
RUN printf "execfile('data/v2/build.py')" | python manage.py shell --settings=config.local

# Expose the app and serve the API.
EXPOSE 8000
CMD python manage.py runserver --settings=config.local 0.0.0.0:8000
