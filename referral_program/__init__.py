from pyramid.config import Configurator
import os


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    db_url = os.environ.get('SQLALCHEMY_URL')
    if db_url:
        settings['sqlalchemy.url'] = db_url
    config = Configurator(settings=settings)
    config.include('.models')
    config.include('.routes')
    #config.include('pyramid_chameleon')

    config.scan('.views')
    return config.make_wsgi_app()
