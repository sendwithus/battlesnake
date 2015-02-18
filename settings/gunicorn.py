""" gunicorn WSGI server configuration. """

from multiprocessing import cpu_count
from os import environ


def max_workers():
    return environ.get('WEB_CONCURRENCY', 1)


bind = '0.0.0.0:' + environ.get('PORT', '8080')

workers = max_workers()
worker_class = 'gevent'  # 'sync'
worker_connections = 1000  # Max active connections at any one time

backlog = 2048  # Max queued connections at any one time
max_requests = 1000  # Recycle each worker after N requests
timeout = 25  # Kill requests after N seconds
