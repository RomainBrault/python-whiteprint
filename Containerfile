# SPDX-FileCopyrightText: © 2023 Romain Brault <mail@romainbrault.com>
#
# SPDX-License-Identifier: MIT

ARG PYTHON_VERSION=3.11
ARG BASE_OS=slim-bullseye

ARG PYTHONDONTWRITEBYTECODE=1
ARG PYTHONBUFFERED=1

ARG VIRTUAL_ENV=/opt/venv

# Use a multi-stage build to reduce the size of the final image.
#   This example is optimized to reduce final image size rather than for
#   simplicity.
# Using a -slim image also greatly reduces image size.
# It is possible to use -alpine images instead to further reduce image size,
# but this comes with several important caveats.
#   - Alpine images use MUSL rather than GLIBC (as used in the default
#   Debian-based images).
#   - Most Python packages that require C code are tested against GLIBC, so
#   there could be subtle errors when using MUSL.
#   - These Python packages usually only provide binary wheels for GLIBC, so
#   the packages will need to be recompiled fully within the container images,
#   increasing build times.
FROM docker.io/python:${PYTHON_VERSION}-${BASE_OS} AS python_builder

# Pin Poetry to a specific version to make container builds reproducible.
ARG POETRY_VERSION=1.4

# Set ENV variables that make Python more friendly to running inside a
# container.
ARG PYTHONDONTWRITEBYTECODE
ARG PYTHONBUFFERED

# Install any system dependencies required to build wheels, such as C
# compilers or system packages For example:
#RUN apt-get update && apt-get install -y \
#    gcc \
#    && rm -rf /var/lib/apt/lists/*

# Install Poetry into a separate virtualenv
#
# TODO: replace pip install -U pip with --upgrade-deps when python 3.8 support
# is dropped
ARG POETRY_ENV=/opt/poetry
RUN python -m venv --symlinks ${POETRY_ENV} && \
    ${POETRY_ENV}/bin/pip install --upgrade pip && \
    ${POETRY_ENV}/bin/pip install "poetry==${POETRY_VERSION}"

# Pre-download/compile wheel dependencies into a virtual environment. Doing
# this in a multi-stage build allows omitting compile dependencies from the
# final image. This must be the same path that is used in the final image as
# the virtual environment has absolute symlinks in it.
#
# TODO: replace pip install -U pip with --upgrade-deps when python 3.8 support
# is dropped
ARG VIRTUAL_ENV
RUN python -m venv --symlinks ${VIRTUAL_ENV} && \
    ${VIRTUAL_ENV}/bin/pip install --upgrade pip
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy in project dependency specification.
ARG WORKDIR=/src
WORKDIR ${WORKDIR}
COPY pyproject.toml poetry.lock ./

# Don't install the package itself with Poetry because it will install it as
# an editable install. TODO: Improve this when non-editable `poetry install`
# is supported in Poetry. https://github.com/python-poetry/poetry/issues/1382
RUN ${POETRY_ENV}/bin/poetry install --only main --no-root

# Copy in source files.
COPY README.md ./
COPY src src

# Manually build/install the package.
RUN ${POETRY_ENV}/bin/poetry build && \
    pip install dist/*.whl && \
    find ${VIRTUAL_ENV} -name '*.pyc' -type f -delete && \
    find ${VIRTUAL_ENV} -name '__pycache__' -type d -delete && \
    find ${VIRTUAL_ENV} -name '*.egg-info' -type d -delete

## Final Image
# The image used in the final image MUST match exactly to the python_builder
# image.
FROM docker.io/python:${PYTHON_VERSION}-${BASE_OS}
MAINTAINER Romain Brault <mail@romainbrault.com>

RUN apt-get update && apt-get install -y \
    git && \
    rm -rf /var/lib/apt/lists/*

# For Python applications that are not installable libraries, you may need to
# copy in source files here in the final image rather than in the
# python_builder image.

# Copy and activate pre-built virtual environment.
ARG VIRTUAL_ENV
COPY --from=python_builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"

# Create the user so the program doesn't run as root. This increases security
# of the container.
ENV USER user
ENV HOME /home/${USER}
RUN addgroup ${USER} && \
    adduser \
    --disabled-password \
    --gecos "" \
    --home "${HOME}" \
    --ingroup "${USER}" \
    "$USER"

# Give access to the entire home folder to the new user so that files and
# folders can be written there. Some packages such as matplotlib, want to write
# to the home folder.

USER user

# Setup application install directory.
ENV APP_HOME ${HOME}/app
RUN mkdir ${APP_HOME}
WORKDIR ${APP_HOME}

ARG PYTHONDONTWRITEBYTECODE
ARG PYTHONBUFFERED
ENV PYTHONDONTWRITEBYTECODE ${PYTHONDONTWRITEBYTECODE} \
    PYTHONBUFFERED ${PYTHONBUFFERED}

ENV WHITEPRINT_HOME ${HOME}/whiteprint
RUN mkdir -p ${WHITEPRINT_HOME}
COPY template/ ${WHITEPRINT_HOME}/template/
COPY jinja_template/ ${WHITEPRINT_HOME}/jinja_template/
COPY copier.yml ${WHITEPRINT_HOME}

ENTRYPOINT ["whiteprint"]

ARG BUILD_DATE
ARG VERSION
ARG REVISION
ARG TAG

LABEL org.opencontainers.image.authors='Romain Brault <mail@romainbrault.com>' \
      org.opencontainers.image.url='https://github.com/RomainBrault/python-whiteprint/pkgs/container/python-whiteprint' \
      org.opencontainers.image.documentation='https://romainbrault.github.io/python-whiteprint/' \
      org.opencontainers.image.source='https://github.com/RomainBrault/python-whiteprint.git' \
      org.opencontainers.image.vendor='Romain Brault' \
      org.opencontainers.image.licenses='MIT' \
      org.opencontainers.image.version=${VERSION} \
      org.opencontainers.image.revision=${REVISION} \
      org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.title='python-whiteprint' \
      org.opencontainers.image.description='A cookiecutter for quick creation of Python projects.' \
      org.opencontainers.image.ref.name=${TAG} \
      org.opencontainers.image.base.name='docker.io/python:'${PYTHON_VERSION}'-'${BASE_OS}
