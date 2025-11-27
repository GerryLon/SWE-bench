_DOCKERFILE_BASE_PHP = r"""
FROM --platform={platform} php:{php_version}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && apt install -y \
    wget \
    git \
    build-essential \
    libgd-dev \
    libzip-dev \
    libgmp-dev \
    libftp-dev \
    libcurl4-openssl-dev \
    && apt-get -y autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install gd zip gmp ftp curl pcntl

RUN curl -sS https://getcomposer.org/installer | php -- --2.2 --install-dir=/usr/local/bin --filename=composer

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

# No env image for PHP. The base image is used as the environment image since it configures the PHP environment

_DOCKERFILE_INSTANCE_PHP = r"""FROM --platform={platform} {env_image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install Python 3.11.8 if not already installed
RUN apt update && apt install -y software-properties-common gnupg && \
    echo "deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu jammy main" > /etc/apt/sources.list.d/deadsnakes-ppa.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 && \
    apt update && \
    apt install -y python3.11 python3.11-venv python3.11-dev python3-pip && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    rm -rf /var/lib/apt/lists/* && \
    python3 --version

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
