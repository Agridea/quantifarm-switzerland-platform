# QuantiFarm Recommendation Tool
The QuantiFarm recommendation tool is an interactive tool that allows farmers and advisors to gain insights on available Digital Agriculture Technology Solutions (DATS) in the QuantiFarm online directory of DATS. The tool can provide recommendations on suitable DATS based on a farms/farmers characteristics and information on results the DATS achieved within test cases.

The tool consists of an API, implemented as a Python [FastAPI](https://fastapi.tiangolo.com/) app, recommendation algorithms, and clients to a triple store database containing the DATS data.
For a direct overview of available API routes, run the app locally and visit in a browser `http://localhost:8000/docs` for the OpenAPI specification.

## Installation
Installation and usage of the tool has the following requirements for your system:
- Python 3.12 or higher installed.
- This repository cloned.
- A working internet connection for connecting to the QuantiFarm central triple store.
- (Optional) Docker installed, with Docker Compose.

## Usage
### Running this app as a Docker container using Compose
1. Navigate to the root folder of this repository.
2. Copy the `.env-default` file and name it `.env`, and fill in the SPARQL endpoint of the triple store containing DATS data. 
3. Build the Docker image using:
    ```bash
    docker compose build
    ```
4. Start a Docker container running the created image, add the `-d`-flag to keep working in the same terminal:
    ```bash
    docker compose up -d
    ```
You can now find the OpenAPI specification of the tool at `http://localhost:8000/docs`.

### Running this app using Python, no Docker
1. Navigate to the root folder of the repository in your terminal.
2. Copy the `.env-default` file and name it `.env`, and fill in the SPARQL endpoint of the triple store containing DATS data. 
3. It is recommended to set up a virtual environment to prevent any issues with missing Python packages. Set this up either with functionalities in your IDE, or with a tool like Astral's [uv](https://docs.astral.sh/uv/), or with these commands: 
    ```bash
    python -m venv .venv
    ```
    The venv needs to be activated, either automatically by your IDE or 
    ```bash
    source ./.venv/bin/activate
    ``` 
    in a bash shell or 
    ```bash
    .\.venv\Scripts\Activate.ps1
    ``` 
    in powershell.
4. Install the required packages with 
    ```bash
    pip install -r requirements.txt
    ```
5. From the root folder of the repository, start the FastAPI app with:  
    ```bash
    uvicorn src.app:app
    ```

You can now find the OpenAPI specification of the tool at `http://localhost:8000/docs`.

## In This Repository
### Additional Documentation
See [docs](./docs/index.md), which is still work in progress.

### Tool Description
The Description of the tool, made specifically for use on the Quantifarm website, can be found in the ``Tool Description.txt`` file, which can be directly placed in the tool description page's div with ``id=tabDescr``.


## Authors and acknowledgment
This recommendation tool is being developed within the [QuantiFarm project](https://quantifarm.eu/), funded under Horizon Europe, as part of the [QuantiFarm toolkit](https://quantifarmtoolkit.eu/). \
The main developers are:
- Daan Di Scala (daan.discala@tno.nl)
- David de Best (david.debest@tno.nl)
- Jack Verhoosel (jack.verhoosel@tno.nl)


## License
The license for this project is yet to be determined.