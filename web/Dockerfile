# Base image
FROM ubuntu:20.04

# Labels and Credits
LABEL \
    name="reNgine" \
    author="Cosmin Craciun (original Yogesh Ojha <yogesh.ojha11@gmail.com>)" \
    description="reNgine is a automated pipeline of recon process, useful for information gathering during web application penetration testing."

# Environment Variables
ENV DEBIAN_FRONTEND="noninteractive" \
    DATABASE="postgres"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install essentials
RUN apt update -y && apt install -y --no-install-recommends \
    build-essential \
    cmake \
    firefox \
    gcc \
    git \
    libpq-dev \
    libpq-dev \
    libpcap-dev \
    netcat \
    postgresql \
    python3 \
    python3-dev \
    python3-pip \
    python3-netaddr \
    wget \
    x11-utils \
    xvfb \
    dnsutils \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    wget \
    libbz2-dev \
    openimageio-tools \
    jq

RUN if [ "$(arch)" = "aarch64" ]; then \
      GO_VERSION=1.22.0.linux-arm64; \
    else \
      GO_VERSION=1.22.0.linux-amd64; \
    fi \
    && wget https://golang.org/dl/go${GO_VERSION}.tar.gz \
    && tar -xvf go${GO_VERSION}.tar.gz \
    && rm go${GO_VERSION}.tar.gz \
    && mv go /usr/local

# Download geckodriver
RUN GK_VERSION=0.34.0 \
    ;if [ "$(arch)" = "aarch64" ]; then \
      GK_ARCH=linux-aarch64; \
    else \
      GK_ARCH=linux64; \
    fi \
    ; wget https://github.com/mozilla/geckodriver/releases/download/v${GK_VERSION}/geckodriver-v${GK_VERSION}-${GK_ARCH}.tar.gz \
    ; tar -xvf geckodriver-v${GK_VERSION}-${GK_ARCH}.tar.gz \
    ; rm geckodriver-v${GK_VERSION}-${GK_ARCH}.tar.gz \
    ; mv geckodriver /usr/bin

# ENV for Go
ENV GOROOT="/usr/local/go"
ENV PATH="${PATH}:${GOROOT}/bin"
ENV PATH="${PATH}:${GOPATH}/bin"

ENV GOPATH=/root/go
ENV PATH="${PATH}:${GOROOT}/bin:${GOPATH}/bin"

# Make directory for app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Download Go packages
RUN go install -v github.com/tomnomnom/assetfinder@latest
RUN go install -v github.com/hakluke/hakrawler@latest

RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
RUN GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
RUN GO111MODULE=on go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
RUN GO111MODULE=on go install -v github.com/tomnomnom/unfurl@latest
RUN GO111MODULE=on go install -v -v github.com/bp0lr/gauplus@latest
RUN GO111MODULE=on go install -v github.com/tomnomnom/waybackurls@latest
RUN GO111MODULE=on go install -v github.com/jaeles-project/gospider@latest
RUN GO111MODULE=on go install -v github.com/tomnomnom/gf@latest
RUN go install -v github.com/owasp-amass/amass/v3/...@master

# Update Nuclei and Nuclei-Templates
RUN nuclei -update
RUN nuclei -update-templates

# Copy requirements
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade setuptools pip && \
    pip3 install -r /tmp/requirements.txt

RUN python3 -m pip install fuzzywuzzy \
    selenium \
    python-Levenshtein \
    pyvirtualdisplay \
    netaddr

WORKDIR /root
RUN wget https://www.python.org/ftp/python/3.10.9/Python-3.10.9.tgz
RUN tar -xf Python-3.10.9.tgz
WORKDIR /root/Python-3.10.9
RUN ./configure --enable-optimizations
RUN make -j $(nproc)
RUN make altinstall
RUN python3.10 -V

RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/maurosoria/dirsearch /usr/src/github/dirsearch
RUN python3 -m pip install -r /usr/src/github/dirsearch/requirements.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/aboul3la/Sublist3r /usr/src/github/Sublist3r
RUN python3 -m pip install -r /usr/src/github/Sublist3r/requirements.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/shmilylty/OneForAll /usr/src/github/OneForAll
RUN python3 -m pip install -r /usr/src/github/OneForAll/requirements.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/FortyNorthSecurity/EyeWitness /usr/src/github/EyeWitness
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/laramies/theHarvester /usr/src/github/theHarvester
RUN python3.10 -m pip install -r /usr/src/github/theHarvester/requirements/base.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/davidtavarez/pwndb /usr/src/github/pwndb

RUN mkdir /root/.gf
RUN cp -r $GOPATH/pkg/mod/github.com/tomnomnom/gf*/examples/*.json /root/.gf
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/1ndianl33t/Gf-Patterns /root/Gf-Patterns
RUN mv /root/Gf-Patterns/*.json /root/.gf

RUN mkdir /usr/src/scan_results
WORKDIR /usr/src/app

# Copy source code
COPY ./tools /usr/src/app/tools

RUN chmod +x /usr/src/app/tools/get_urls.sh
