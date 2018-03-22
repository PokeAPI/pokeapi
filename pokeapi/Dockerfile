# Build the app on top of Ubuntu
FROM ubuntu:xenial

RUN echo 'deb http://ppa.launchpad.net/chris-lea/redis-server/ubuntu xenial main' > /etc/apt/sources.list.d/redis-server.list && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7917B12

# Patch and Install Dependencies
RUN apt-get -y update && apt-get -y install git python-dev make python-pip libpq-dev postgresql postgresql-contrib redis-server && apt-get -y clean

# Updating redis config
RUN sed -i 's/# bind 127\.0\.0\.1/bind 127\.0\.0\.1/' /etc/redis/redis.conf

CMD mkdir -p /app && chown -R postgres:postgres /app

# Add python requirements to the image
ADD requirements.txt /app/requirements.txt
ADD test-requirements.txt /app/test-requirements.txt

# Set a working directory
WORKDIR /app/

# Build the application
RUN pip install --no-cache-dir -r requirements.txt

# Add the application code to the image
ADD . /app/

# Start postgres database and use it while it is running in the container
# Create the default db user (ash) 
RUN service postgresql start                                 && \
    service redis-server start                               && \
    su - postgres -c "psql --command \"CREATE USER ash WITH PASSWORD 'pokemon'\"" 	&& \
    su - postgres -c "createdb -O ash pokeapi"                                  	&& \
    python manage.py migrate --settings=config.docker                         		&& \
    echo "from data.v2.build import build_all; build_all(); quit()" | python -u manage.py shell --settings=config.docker

# Expose the app and serve the API.
EXPOSE 8000
CMD service postgresql start && service redis-server start && python manage.py runserver --settings=config.docker 0.0.0.0:8000
