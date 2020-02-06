from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('hello', '/hello')
    #config.add_route('get_ap_scan_status', '/ap_scan/{id}/status')
    #config.add_route('get_ap_scan_results', '/ap_scan/{id}/results')
    config.scan('.views')
    return config.make_wsgi_app()
