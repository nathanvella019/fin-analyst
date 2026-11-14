# Understanding and running the API and Docker

## What the pieces do

Python code already answers questions. An API gives another program a way to call it over HTTP. FastAPI checks the input and routes the request; Uvicorn listens for requests. A client sends a JSON object to `POST /ask`, and receives a JSON response. POST means send a request body. `/ask` names the endpoint. HTTP 200 means processing succeeded, not that the financial answer is correct. HTTP 422 means the request is invalid.

Docker builds an image: Python, Linux environment, dependencies, our package and startup command. A container is a running instance of that image. Docker Desktop manages the Linux VM on a Mac. Compose records how to build and start the container so you do not need to remember a long `docker run` command.

The database engine runs inside the container. The Parquet files remain in the Mac's project folder and are attached read-only. This is called a bind mount. The original notebook and raw JSON files are not needed to serve already prepared data.

```text
Client sends JSON → POST /ask → existing parser and SQL → DuckDB reads Parquet
Client receives JSON ← candidate, provenance and review decision ← query result
```

## Before starting

Run from `fin-analyst`. Have Docker Desktop running. Prepare all four quarters with `python3 -m sec_analyst.prepare`, then run `python3 -m sec_analyst.evaluate_policy` once to prepare the line-item cache. Both steps require the installed project environment. The service needs the 16 quarterly Parquet files and `08_line_items.parquet` in `data/processed/`.

## Start and inspect

```bash
docker compose up --build -d
docker compose ps
docker compose logs --tail=30 api
```

`up` creates/starts the service, `--build` builds its image, and `-d` leaves it running in the background. Startup loads the mapper before requests are accepted. `ps` lists the service state. `logs` shows what the server reported.

Open http://localhost:8008/docs for the interactive request form. Expand POST /ask, choose Try it out, enter the JSON below and Execute:

```json
{"question": "What was Birner Dental Management Services's revenue in fiscal 2015?"}
```

Or send it from your terminal:

```bash
curl -sS http://localhost:8008/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"What was Birner Dental Management Services revenue in fiscal 2015?"}'
```

`curl` is the client. `-H` identifies the input as JSON; `-d` sends the body and selects POST. The Birner candidate is 63,843,837. `candidate` is the model's proposed result, `provenance` identifies its filing, and `signals` records warning signs. All responses remain `decision: refer`, with `answer: null`, because the known FutureFuel mistake prevents operational release. `passes_notebook_filter: true` does not override that restriction.

To stop the service:

```bash
docker compose down
```

This removes the running service container/network, not your source files or mounted dataset. The image remains available for another start.

## Running without Docker

```bash
source .venv/bin/activate
python3 -m uvicorn sec_analyst.api:app --host 127.0.0.1 --port 8008 --workers 1
```

Stop the container first so both servers do not compete for port 8008. Press Ctrl+C to stop the terminal server.

## Tests

```bash
python3 -m unittest discover -s tests -v
docker compose run --rm --no-deps api python -m unittest discover -s tests -v
```

The small tests check request validation, connection cleanup and deliberate wrong-context data. Real-data comparison evidence is recorded separately. Docker passing these tests is not the full golden-set release gate.

Reference documentation: [FastAPI lifecycle](https://fastapi.tiangolo.com/advanced/events/) and [Docker bind mounts](https://docs.docker.com/engine/storage/bind-mounts/).

The Mac already had port 8000 in use. Compose maps host port 8008 to container port 8000; these are separate network spaces.
