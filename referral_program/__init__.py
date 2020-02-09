from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include('.models')
    config.include('.routes')
    #config.include('pyramid_chameleon')

    config.scan('.views')
    return config.make_wsgi_app()
