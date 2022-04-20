FROM postgres
WORKDIR /app
RUN apt-get update
RUN apt-get install -y \
    software-properties-common
RUN apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip

RUN apt-get install -y --no-install-recommends \
    "postgresql-plpython3-$PG_MAJOR"

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .
RUN pip3 install -e ./
