# top-250-website
Website-hosted dashboard showing analysis of the Top 250 Filipino Movies of all time.

For curious developers and data enthusiasts, I've set-up a couple of guides that you can access below to understand how I
arrived at this project.

### Guides
- [Docker Setup](/docs/docker_setup.md)
- Fast API (Coming soon)


### Instructions for activating (dev-only)
1. Save as shell script something like `run_fastapi.sh`.
2. In `run_fastapi.sh`,

```bash
uvicorn main:app --reload
```
Be sure that the uvicorn (Python Web Server implementation) is installed before executing the script.

3. (Optional) To make easier execution, execute the following query in the terminal. This adds an execute permission to the file.
```bash
chmod +x ./run_fastapi.sh
```
This will allow run_fastapi.sh, which is installed in your project's working folder, to be executed when typing said file down as it has an execute permission.

### Version
```
    0.0.1
```

### Changelogs
```
    Coming soon!
```

### Pipeline Model
![](model_flowchart.png)

The back-end consists of an API built using Python's FastAPI and points to the MongoDB database. The front-end is powered via Vue.js (Nuxt) which interacts with the API to retrieve data that will be shown on the front-end.

#### Authors
Jay Cruz
