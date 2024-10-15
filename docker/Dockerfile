FROM python:3.11-slim

ENV HOME=/root
ENV \
    PYTHONBUFFERED=1 \
    VIRTUAL_ENV="${HOME}/venv" \
    PATH="/usr/local/gcloud/google-cloud-sdk/bin/:${PATH}" \
    PYTHONPATH="/app:${PYTHONPATH}" \
    DEBIAN_FRONTEND="noninteractive" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TZ=Asia/Seoul

RUN apt-get update \
    && apt-get -qq -y install git curl wget vim \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

# Install gcloud and gsutils
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-462.0.1-linux-x86_64.tar.gz \
    && mv /google-cloud-cli-462.0.1-linux-x86_64.tar.gz /tmp/google-cloud-cli-462.0.1-linux-x86_64.tar.gz
RUN mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -zxf /tmp/google-cloud-cli-462.0.1-linux-x86_64.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh \
		--usage-reporting false --command-completion true --bash-completion true --path-update true --quiet

COPY ./docker/scripts/*.sh /

RUN chmod a+x /*.sh \
    && mkdir -p /app

COPY . /app
WORKDIR /app

RUN python3.11 -m venv ${VIRTUAL_ENV} \
    && pip install --upgrade pip setuptools \
    && pip install -r requirements.txt \
    && rm -rf ${HOME}/.cache/*

ENTRYPOINT ["/bin/bash"]
CMD ["/run-server.sh"]
EXPOSE 8000