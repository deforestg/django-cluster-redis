# django-cluster-redis
- Supports AWS ElasticCache and any other similar style redis.
- The breaking difference in functionality is that ElasticCache often returns "MOVED 9134 {ip}:6379" with an ip address that you need to follow.
- This code follows those "MOVED" responses and reuses existing connections when available.

## Compatibility
- python 2.7, and >=3.4
- django >= 1.8.x

## Installation

### pip
pip install django-cluster-redis


## Configuration

### django settings

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'YOUR REDIS CLUSTER HERE',
        'OPTIONS': {
            'REDIS_CLIENT_CLASS': 'django_cluster_redis.cache.ClusterRedis',
        }
    }
}
```


## Build and run tests

- `tox -r`
