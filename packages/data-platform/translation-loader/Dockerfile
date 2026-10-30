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

COPY translation-loader /app/translation-loader
WORKDIR /app/translation-loader/
RUN python setup.py bdist_wheel
RUN pip install ./dist/*.whl

# Pre-exported translation JSON files for TRANSLATIONS_LOAD_FROM_JSON mode.
# Generate with: python -m translation_loader.exporter
COPY translation-loader/translations-dats.json /data/translations-dats.json
COPY translation-loader/translations-testcases.json /data/translations-testcases.json

ENTRYPOINT [ "python", "-m", "translation_loader" ]
