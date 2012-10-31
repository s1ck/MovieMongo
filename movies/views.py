from bottle import route, TEMPLATE_PATH, jinja2_template as template

TEMPLATE_PATH.append("./movies/templates")

@route('/')
def index():
    return template("index.html")
