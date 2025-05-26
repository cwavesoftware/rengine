# Base image
FROM ubuntu:22.04

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
    gcc \
    git \
    libpq-dev \
    libpq-dev \
    libpcap-dev \
    netcat \
    postgresql \
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
    jq \
    unzip \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxdamage1 \
    libasound2

# python
RUN apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update -y \
    && apt install -y python3.10-dev
RUN apt install -y python3.10-distutils
RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py
COPY ./requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade setuptools pip && \
    python3 -m pip install --no-build-isolation -r /tmp/requirements.txt

# python 3.10 is default on ubuntu 22.04
RUN python3 -V
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/maurosoria/dirsearch /usr/src/github/dirsearch
RUN python3 -m pip install -r /usr/src/github/dirsearch/requirements.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/aboul3la/Sublist3r /usr/src/github/Sublist3r
RUN python3 -m pip install -r /usr/src/github/Sublist3r/requirements.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/shmilylty/OneForAll /usr/src/github/OneForAll
RUN python3 -m pip install -r /usr/src/github/OneForAll/requirements.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/laramies/theHarvester /usr/src/github/theHarvester

RUN python3 get-pip.py
RUN python3 -m pip install -r /usr/src/github/theHarvester/requirements/dev.txt
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/davidtavarez/pwndb /usr/src/github/pwndb

# go
RUN if [ "$(arch)" = "aarch64" ]; then \
      GO_VERSION=1.22.0.linux-arm64; \
      wget https://playwright.azureedge.net/builds/chromium/1067/chromium-linux-arm64.zip; \
      unzip chromium-linux-arm64.zip -d /opt/; \
    else \
      GO_VERSION=1.22.0.linux-amd64; \
      wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1131003/chrome-linux.zip; \
      unzip chrome-linux.zip -d /opt/; \
      # geckodriver (used by EyeWitness) won't work on Apple Silicon chips, will break at runtime
      # Download geckodriver
      wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz; \
      tar -xvf geckodriver-v0.32.0-linux64.tar.gz; \
      rm geckodriver-v0.32.0-linux64.tar.gz; \
      cp geckodriver /usr/bin; \
      cp geckodriver /usr/sbin; \
      git clone --branch v20230525.1 --single-branch https://${GITHUB_USER}:${GITHUB_PASS}@github.com/FortyNorthSecurity/EyeWitness /usr/src/github/EyeWitness; \
      bash /usr/src/github/EyeWitness/Python/setup/setup.sh; \
      pip uninstall --no-input -y selenium; \
      pip install selenium==4.9.1; \
    fi \
    && wget https://golang.org/dl/go${GO_VERSION}.tar.gz \
    && tar -xvf go${GO_VERSION}.tar.gz \
    && rm go${GO_VERSION}.tar.gz \
    && mv go /usr/local

# ENV for Go
ENV GOROOT="/usr/local/go"
ENV GOPATH=/root/go
ENV PATH="${GOROOT}/bin:${GOPATH}/bin:${PATH}"

# Make directory for app
WORKDIR /usr/src/app

# Download Go packages
RUN go install -v github.com/tomnomnom/assetfinder@latest
RUN go install -v github.com/hakluke/hakrawler@latest
RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@v1.6.9
RUN GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@v2.6.6
RUN GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@v3.3.5
RUN GO111MODULE=on go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@v2.3.1
RUN GO111MODULE=on go install -v github.com/tomnomnom/unfurl@latest
RUN GO111MODULE=on go install -v -v github.com/bp0lr/gauplus@latest
RUN GO111MODULE=on go install -v github.com/tomnomnom/waybackurls@latest
RUN GO111MODULE=on go install -v github.com/jaeles-project/gospider@latest
RUN GO111MODULE=on go install -v github.com/tomnomnom/gf@latest
RUN go install -v github.com/owasp-amass/amass/v3/...@master

# Update Nuclei and Nuclei-Templates
RUN nuclei -update
RUN nuclei -update-templates

RUN mkdir /root/.gf
RUN cp -r $GOPATH/pkg/mod/github.com/tomnomnom/gf*/examples/*.json /root/.gf
RUN git clone https://${GITHUB_USER}:${GITHUB_PASS}@github.com/1ndianl33t/Gf-Patterns /root/Gf-Patterns
RUN mv /root/Gf-Patterns/*.json /root/.gf

RUN mkdir /usr/src/scan_results

# firefox
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F
RUN add-apt-repository ppa:mozillateam/ppa
RUN echo 'Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001\n\nPackage: firefox\nPin: version 1:1snap*\nPin-Priority: -1' | tee /etc/apt/preferences.d/mozilla-firefox
RUN apt update -y && apt install firefox -y --allow-downgrades

# Copy source code
COPY ./tools /usr/src/app/tools
RUN chmod +x /usr/src/app/tools/get_urls.sh
