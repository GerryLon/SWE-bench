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

# Install Python 3.11 from Debian repositories
RUN echo "deb https://mirrors.cloud.tencent.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb https://mirrors.cloud.tencent.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.cloud.tencent.com/debian-security/ bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    apt update && \
    apt install -y python3 python3-pip python3-venv python3-dev && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    rm -rf /var/lib/apt/lists/* && \
    python3 --version

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
