"""
External endpoint to the duel package.
This has to be run from one level outside the package
"""
import json
import docker

from duel import app, socketio

import duel

def main():
    """
    Loads the configuration from JSON and initalizes the necessary modules
    """
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
    except IOError:
        exit('Missing Config File: config.json')
    
    env = config.get('environment', '')
    if not env:
        exit('Missing environment in config.json')

    config = config.get(env, {})
    if not config:
        exit('Missing configuration in config.json')

    duel.config = config

    duel.docker_client = docker.Client(**config['docker'])
    app.secret_key = config['secret_key']
    app.debug = config['debug']
    socketio.run(app, **config['app'])

if __name__ == '__main__':
    """
    Monkey patch's all functions before launching to allow for
    proper async via gevent
    """
    from gevent import monkey
    monkey.patch_all()
    main()
