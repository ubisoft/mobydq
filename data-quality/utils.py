import jinja2

def updateQuery(query, parameters):
    template = jinja2.Template(query)
    query = template.render(parameters)
    return(query)