FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /code/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /code/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/code

COPY ./scripts/ /code/

COPY ./alembic.ini /code/

COPY ./prestart.sh /code/

COPY ./tests-start.sh /code/

COPY ./app /code/app

CMD ["uvicorn", "app.main:app"]