import pkgutil

from jinja2 import Environment, FunctionLoader


def _load_template(name):
    template = pkgutil.get_data('cert.templates', name)
    assert template, 'Template "%s" not found' % name
    return template.decode()
env = Environment(loader=FunctionLoader(_load_template))


def render(template, **context):
    return env.get_template(template).render(context)
