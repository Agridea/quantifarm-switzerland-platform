FROM python:3.11.4-slim

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

COPY testcase-loader /app/testcase-loader
WORKDIR /app/testcase-loader/
RUN python setup.py bdist_wheel
RUN pip install ./dist/*.whl

ENTRYPOINT [ "python", "-m", "testcase_loader" ]
