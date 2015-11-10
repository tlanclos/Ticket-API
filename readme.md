# Techneaux Ticket API

## Project structure layout

### Abstract

> By reading this, you will understand the basic structure/layout of the structure of this project, its components, and which interfaces are involved in the implementation of this project with the operating system. What is listed below is the output of the Linux command `tree`. This command provides some insight of the structure of this project--specificly the directory structure.

```
.
├── config
│   ├── build.md
│   ├── Makefile
│   └── ticket-api.conf
├── Makefile
├── readme.md
├── ticketapi
│   ├── apps
│   │   ├── __init__.py
│   │   ├── nossl.py
│   │   ├── genauth.py
│   │   └── ticketapi.py
│   ├── data
│   │   ├── crypt.py
│   │   ├── decorators.py
│   │   ├── fields.py
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── response.py
│   │   ├── test-pepper.json
│   │   └── validators.py
│   ├── datalayer
│   │   ├── __init__.py
│   │   ├── makedb.py
│   │   ├── models.py
│   │   ├── procedures.py
│   │   └── wrapper.py
│   ├── __init__.py
│   ├── Makefile
│   ├── nossl.wsgi
│   ├── runserver.py
│   └── ticketapi.wsgi
├── tools
│   ├── sendrequest.py
│   └── testlogin.json
└── vars.mk
```

### Config directory

> I will start by mentioning the configuration directory `config`. Within this directory there are only a few files. One file `build.md` provides step-by-step instructions on how to build this server from the state provided by Techneaux--I am assuming this was a minimal install of Ubuntu server.  This API runs off of the Apache web server, so there must be a configuration associated with it. This configuation is `config/ticket-api.conf`. In this file, there is the appropriate configuration for both applications. One application that runs on port 443 (the real ticket API app) and one that runs on port 80 (the app that always tells the user to connect via SSL before using the API).

### Tools directory

> This directory will contain tests that will be used to test the API's functionality when functionality testing is needed. Currently, there is a script called `sendrequest.py`. This script will simply ready in some JSON definition (test) files and run them. This will be extended upon in the future.

### Makefile structure

> This project utilizes GNU Make to build and deploy the API. Under ideal circumstances, a Debian package should be created to install via `apt-get`, but unfortunately we will not have time to research and create this package. For the time being, this repository may be cloned, extended upon, make'd and make install'd. There are a few base files to this make system:

> - `vars.mk` - this file contains all base definitions for directories that may be touched or used
> - `Makefile` - the base makefile for the system. This file will run all sublevel makes in the approriate order

> All other makefiles are specific to the directory in which they are located

### Ticketapi directory

> Last, there is the `ticketapi` directory which contains all logic, applications, classes, and wsgi files that are associated with the ticket API itself. In the following, I will provide a brief description of each files, but I will first explain all `__init__.py` files. Each `__init__.py` file references a package in Python. That is, if `__init__.py` is located under the directory `ticketapi`, now `ticketapi` is considered a package. Each of these files contain the major imports and globals for a given package.

> - `ticketapi.wsgi` - wsgi app containing the logic for stating the ticketapi app located in `ticketapi.apps`
> - `nossl.wsgi` - wsgi app containing the logic for starting the nossl app located in `ticketapi.apps`
> - `datalayer/` - this directory contains all methods and logic for interfacing with the provided database
>   - `makedb.py` - this script may be used to create the tables, etc structure using the provided database configuration
>   - `models.py` - these are the models associated with tables located within the database
>   - `procedures.py` - any procedure that is associated with functionality of a mapping between API and the database is located here
>   - `wrapper.py` - contains a simple database session wrapper that may be used to grab the database session and query the database
> - `data/` - this directory contains all the basic data handling objects
>   - `crypt.py` - library that will contain all cryptographic functionality required to encrypt and test passwords
>   - `decorators.py` - any decorator that may be used to decorate a function for validation, authentication, etc. is located here
>   - `fields.py` - this file contains the field types that may be used to validate a request field via the validators classes
>   - `logger.py` - contains the global logger that will be used to log anything
>   - `response.py` - all response types that may be standardized are located within here such as `FailureResponse`
>   - `validators.py` - contains all validator types that may be used to validate fields within a request
> - `apps/` - all major flask applications that are the entry point to code execution
>   - `nossl.py` - this app is one that will always respond with a message telling the user to connect via SSL
>   - `ticketapi.py` - this is the main app that will run all URIs required by the specification of this project
>   - `genauth.py` - this app is a CLI utility to generate rows in the Authentication column used for authorizing a company









.
