# Spotted
## Developers Institute - Final Project
A VueJS / Flask web application that allows users to geotag locations of interest using the Google Maps API, attach a description and add pictures.

[![Netlify Status](https://api.netlify.com/api/v1/badges/038c1a83-f4b5-4b9d-9bb0-20ebc3f1e654/deploy-status)](https://app.netlify.com/sites/cool-as-code-secretly/deploys)  
*Demo*: https://spotted.joeri.xyz/

![Spotted Screenshot](spotted.png)

*Usage Instructions:*
- Register an account and login, or login using the demo credentials:  
demo@foo.bar / rabooftaomed

# spotted-client
The Spotted frontend, built with VueJS/Vite and TailwindCSS.

Features:
- Computed Properties
- Class and Style bindings
- Conditional rendering
- Pinia State Management
- Event handling
- Lifecycle hooks


### Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

# spotted-api
The Spotted backend, a REST API built with Python & the Flask framework.

### Project Setup

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r spotted-api/requirements.txt
```

### Run Development Server

```sh
python3 spotted-api/app.py
```

### Or using Podman (or Docker)
```shell
cd spotted-api
podman build --tag spotted-api -f Dockerfile
podman run --name mySpottedApiContainerName -p 8080:8080 spotted-api
```
