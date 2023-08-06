# Paramo
**Paramo** is a library for HTTP parameter (Query) parsing.<br>
It acts much like a common CLI argument parser, letting you adding default values.

# Installation
```sh
# Git + Pip
pip install git+https://github.com/ZSendokame/Paramo

# Pip
pip install Paramo
```

# Use
```py
import paramo
from flask import Flask, request

app = Flask(__name__)
params = paramo.Parser()


@app.before_request
def before():
    params.add('name', default='Drackord')
    params.add('role', default='The lost son of Julio Iglesias')
    params.parse(request.url)


@app.get('/')
def root():
    params.query_list['unparsed'] = paramo.unparse(params.query_list)

    return params.query_list


app.run()

# url: http://127.0.0.1:5000/?surname=Iglesias
# {
#   "name": "Drackord",
#   "role": "The lost son of Julio Iglesias",
#   "surname": "Iglesias",
#   "unparsed": "?surname=Iglesias&name=Drackord&role=The lost son of Julio Iglesias"
# }
```