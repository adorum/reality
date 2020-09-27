import os

broker_url = os.environ.get("WORKER_REDIS_URL", 'redis://localhost:6379/0')
result_backend = 'redis://localhost:6379'
