from redis.client import StrictRedis
from redis.exceptions import ResponseError


class ClusterRedis(StrictRedis):
    def _action(self, action_type, *args, **kwargs):
        method = getattr(super(ClusterRedis, self), action_type)
        try:
            return method(*args, **kwargs)
        except ResponseError as e:
            msg = str(e)
            if 'MOVED' not in msg:
                raise e

            # parse out the address and port number
            msg_split = msg.rsplit(' ')[2].rsplit(":")
            host = msg_split[0]
            port = msg_split[1]
           
            self._follow_redirect(host, port)

            return method(*args, **kwargs)

    def _follow_redirect(self, host, port):
        pool = self.connection_pool

        pool.connection_kwargs['host'] = host
        pool.connection_kwargs['port'] = port
        available_connections = pool._available_connections

        # find existing connection to reuse - redis always pops off the last connection
        connection = [c for c in available_connections if c.host == host and c.port == int(port)]

        if connection:
            connection = connection[0]
            available_connections.remove(connection)
        else:
            connection = pool.make_connection()

        available_connections.append(connection)

    def get(self, *args, **kwargs):
        return self._action('get', *args, **kwargs)

    def set(self, *args, **kwargs):
        return self._action('set', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._action('delete', *args, **kwargs)

    def delete_many(self, *args, **kwargs):
        return self._action('delete_many', *args, **kwargs)

    def delete_pattern(self, *args, **kwargs):
        return self._action('delete_pattern', *args, **kwargs)

    def exists(self, *args, **kwargs):
        return self._action('exists', *args, **kwargs)

    def dump(self, *args, **kwargs):
        return self._action('dump', *args, **kwargs)

    def expire(self, *args, **kwargs):
        return self._action('expire', *args, **kwargs)

    def move(self, *args, **kwargs):
        return self._action('move', *args, **kwargs)

    def decr(self, *args, **kwargs):
        return self._action('decr', *args, **kwargs)

    def flushall(self, *args, **kwargs):
        return self._action('flushall', *args, **kwargs)

    def flushdb(self, *args, **kwargs):
        return self._action('flushdb', *args, **kwargs)

    def ttl(self, *args, **kwargs):
        return self._action('ttl', *args, **kwargs)

    def type(self, *args, **kwargs):
        return self._action('type', *args, **kwargs)

    def rename(self, *args, **kwargs):
        return self._action('rename', *args, **kwargs)

    def keys(self, *args, **kwargs):
        return self._action('keys', *args, **kwargs)

    def mget(self, *args, **kwargs):
        return self._action('mget', *args, **kwargs)

    def mset(self, *args, **kwargs):
        return self._action('mset', *args, **kwargs)

    def msetnx(self, *args, **kwargs):
        return self._action('msetnx', *args, **kwargs)

    def persist(self, *args, **kwargs):
        return self._action('persist', *args, **kwargs)

    def pexpire(self, *args, **kwargs):
        return self._action('pexpire', *args, **kwargs)

    def pexpireat(self, *args, **kwargs):
        return self._action('pexpireat', *args, **kwargs)

    def psetex(self, *args, **kwargs):
        return self._action('psetex', *args, **kwargs)

    def pttl(self, *args, **kwargs):
        return self._action('pttl', *args, **kwargs)

    def randomkey(self, *args, **kwargs):
        return self._action('randomkey', *args, **kwargs)

    def renamenx(self, *args, **kwargs):
        return self._action('renamenx', *args, **kwargs)

    def restore(self, *args, **kwargs):
        return self._action('restore', *args, **kwargs)

    def lrange(self, *args, **kwargs): 
        return self._action('lrange', *args, **kwargs)

    def lpush(self, *args, **kwargs): 
        return self._action('lpush', *args, **kwargs)
