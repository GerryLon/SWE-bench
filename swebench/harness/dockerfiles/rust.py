# If you change the base image, you need to rebuild all images (run with --force_rebuild)
_DOCKERFILE_BASE_RUST = r"""
FROM --platform={platform} rust:{rust_version}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && apt install -y \
wget \
git \
build-essential \
&& rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

_DOCKERFILE_INSTANCE_RUST = r"""FROM --platform={platform} {env_image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install Python 3.11.8 if not already installed
RUN apt update && apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
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
