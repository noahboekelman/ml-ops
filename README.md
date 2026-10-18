# How to run
These are some instructions on how to run this project.

## Prerequisites
* We need to install the package manager that we are using for this project. This pkg manager is called `uv` and is a great option in terms of speed and efficiency.
* The Python version is defined in `.python-version`. UV installs this automatically though, so it's not necessarily needed.
* We will also need to have `Docker Desktop` installed, if we want to build and run the container. If we're on a Mac it is recommended that we use `OrbStack` though, as this is a faster and more light-weight alternative to Docker Desktop :)

## Running the API
Before running the API we need to first sync the dependencies with `uv`. Dependencies are defined in `pyproject.toml`.

```bash
uv sync --dev # with dev dependencies
```

After we've synced our dependencies using our `uv` package manager we need to activate our virtual environment. We use a virtual environment because we don't want to install all of these packages on our machine *globally*. This is done in different ways, depending on if we're on a Mac/Linux or a Windows machine.
### Activate the virtual environment on Windows
From root (PowerShell):

```powershell
.venv\Scripts\activate
```

### Activate the virtual environment on macOS/Linux
From root (zsh):

```bash
source .venv/bin/activate
```

### Starting the API
After we've activated our virtual environment we can start the API.

```bash
uv run fastapi dev app/main.py
```

We will find the server running locally on `http://localhost:8000/docs`.

### Dashboard
A dashboard has been created for nurses, as per the instructions of the assignment.

We find the dashboard at: `http://localhost:8000/dashboard`.

## How to run Docker
First we build the Docker image and then we run the container.

### Building the image
From root:

```bash
docker build -t ml-ops .
```

### Running the container (on port 80)
From root:

```bash
docker run -p 80:80 ml-ops
```

We will find the container (with the API) running locally on `http://localhost:80/docs`.

# Pipelines and Releases
We currently have three Github Workflows that runs actions.
* **ci.yaml**: Runs on each PR and is also called by `cicd.yaml` and `release.yaml`.
* **cicd.yaml**: Runs on pushes and merges to main.
* **release.yaml**: Runs on tag operations (prefixed with `v`).

For each build (cicd and release) we push the image to GHCR.

## Images
All images are pushed to `ghcr.io/noahboekelman/ml-ops` with different tags per workflow:

* **cicd.yaml**: `ghcr.io/noahboekelman/ml-ops:<commit-sha>`
* **release.yaml**: `ghcr.io/noahboekelman/ml-ops:<version>`, `ghcr.io/noahboekelman/ml-ops:<major>.<minor>` and `ghcr.io/noahboekelman/ml-ops:latest`

## Example Release
We always tag from main.
Tags are always prefixed with `v`.

```bash
git checkout main
git pull
```
To create and push a release tag, we use **annotated tags** to include release notes:

```bash
git tag -a v0.0.1 -m "First release
- <Some release note>
- <Some other release note>"
git push origin v0.0.1
```

We can also create and push a tag with the release notes from a markdown file:
```bash
git tag -a v0.0.1 -F release-notes-v0.0.1.md
git push origin v0.0.1
```



# Links
[Python Download](https://www.python.org/downloads/)

[UV Installation](https://docs.astral.sh/uv/getting-started/installation/)

[Docker Installation](https://docs.docker.com/get-docker/)

[OrbStack Download](https://orbstack.dev/download)

[Git Tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging)