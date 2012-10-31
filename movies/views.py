from bottle import static_file, route, TEMPLATE_PATH, jinja2_template as template

TEMPLATE_PATH.append("./movies/templates")

# @route('/media/<filename>')
# def server_static(filename):
#     return static_file(filename, root='media')
@route('/media/:path#.+#', name='static')
def static(path):
    return static_file(path, root='media')

@route('/')
def index():
    return template("index.html")

