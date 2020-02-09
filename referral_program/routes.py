def includeme(config):
    config.add_route('hello', '/hello')
    config.add_route('create_user', '/user')
    config.add_route('create_referral', '/user/{user_id}/referral')