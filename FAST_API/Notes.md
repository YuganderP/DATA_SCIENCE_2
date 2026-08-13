

## part 1

## introduction 

install fast api 
create a basic app, build routes which returns json
create api end points, html responses 



## uv to install packages or we can simply use pip 

# uv init fastapi_blog # create an empty project 
# uv add fastapi[standard]
# pip install 'fastapi[standard]
# fastapi standard includes : py
# fast api uses decorators for routes 

# to Run the application fastapi dev main.py ( dev mode included auto reload )
# fastapi run main.py ( in production environment )

# to Run the application uvicorn main:app --reload

# fast api Feature : automatic API documentation 

# localhost: url /docs -> takes to api doc ( created automatically)


### to return HTML response 
we need to import HTML response

from fastapi.responses import HTMLResponse 

@app.get("/",response_class=HTMLResponse) # fast api uses decorators for routes 
def home(): # regular sync function 
    return f"<h1>{posts[0]['title']}</h1>"



## part 2 

#### Jinja 2 Templates and API front end

## how to use templates, pass data to templates, while maintaining json output for backends
## jinja 2 templates for for loop and conditionals
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI,Request

