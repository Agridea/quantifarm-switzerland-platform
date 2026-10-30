FROM python:3.11.4-alpine

# Create and enable venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install wheel

WORKDIR /app/

COPY common /app/common
WORKDIR /app/common/
RUN python setup.py bdist_wheel
RUN pip install ./dist/*.whl

COPY dats-loader /app/dats-loader
COPY dats-loader/*.json /data/
COPY dats-loader/*.xls /data/
WORKDIR /app/dats-loader/
RUN python setup.py bdist_wheel
RUN pip install ./dist/*.whl

ENTRYPOINT [ "python", "-m", "dats_loader" ]
