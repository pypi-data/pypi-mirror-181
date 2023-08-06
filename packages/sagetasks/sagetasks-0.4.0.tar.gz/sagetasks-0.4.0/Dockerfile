FROM python:3.10.6

WORKDIR /usr/src/app

ARG PKG_VERSION=1

RUN pip install --no-cache-dir pipenv

COPY setup.* Pipfile* ./
COPY src ./src/

RUN SETUPTOOLS_SCM_PRETEND_VERSION_FOR_SAGETASKS=${PKG_VERSION} \
    pipenv install --system

CMD [ "python", "-c", "import sagetasks" ]
