# API

## Setup project

### Prerequisites
- `python@3.8` or above

### Setup python virtual env

In this directory, there's a `bash` script that will setup the api environment for you. You just need to execute:

`./setup.sh`

If you want to do it manually, follow these instructions:

#### 1) Install virtualenv (you can use other virtual environment tool if you want)
`python3 -m pip install virtualenv`

#### 2) Setup virtualenv
`virtualenv EngSoftEnv`

obs: EngSoftEnv is the virtual env declared in .gitignore. If you want to name it to something else, remember to place the generated folder name in .gitignore

#### 3) Install requirements

`python -m pip install -r requirements.txt`

#### 4) Run the project

`flask run`

## Backend Requirements

### User CRUD
- [ ] new account
- [ ] login
- [ ] logout
- [ ] forgot password
- [ ] exclude account
- [ ] update personal data

### CRUD products
new product
delete product
edit product
get product
list products

### CRUD basket
add product to basket
remove product from basket
edit amount of product


## FRONTEND  

