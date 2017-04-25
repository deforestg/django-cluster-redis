from flexmock import flexmock
from unittest import TestCase
from redis.client import StrictRedis
from redis.exceptions import ResponseError
from django_cluster_redis.cache import ClusterRedis


class FakeConnection:
    host = None

    def __init__(self, host):
        self.host = host


class CacheTestCase(TestCase):
    def setUp(self):
        super(CacheTestCase, self).setUp()
        self.base_redis_mock = flexmock(StrictRedis)
        self.redis = ClusterRedis()

    def test_intercept_action(self):
        self.base_redis_mock.should_receive('get').with_args('test').and_return('asdf')
        value = self.redis.get('test')
        self.assertEqual(value, 'asdf')

    def test_follows_move(self):
        self.base_redis_mock.should_receive('set').with_args('test', 'asdf')\
            .and_raise(ResponseError, 'MOVED 9134 123.test.ip.321:6379').ordered().once()
        self.base_redis_mock.should_receive('set').with_args('test', 'asdf')\
            .and_return('foo').ordered().once()

        mock_pool = flexmock(connection_kwargs={}, _available_connections=[])
        mock_pool.should_receive('make_connection').with_args().and_return('fake connection')
        self.redis.connection_pool = mock_pool
        value = self.redis.set('test', 'asdf')
        self.assertEqual(value, 'foo')
        self.assertEqual(mock_pool._available_connections, ['fake connection'])

    def test_reuses_existing_connection(self):
        self.base_redis_mock.should_receive('set').with_args('test', 'asdf')\
            .and_raise(ResponseError, 'MOVED 9134 123.test.ip.321:6379').ordered().once()
        self.base_redis_mock.should_receive('set').with_args('test', 'asdf')\
            .and_return('foo').ordered().once()

        conn_1 = FakeConnection('asdf')
        conn_2 = FakeConnection('123.test.ip.321')
        conn_3 = FakeConnection('fdsa')
        fake_connections = [conn_1, conn_2, conn_3]
        mock_pool = flexmock(connection_kwargs={}, _available_connections=fake_connections)
        self.redis.connection_pool = mock_pool
        value = self.redis.set('test', 'asdf')
        self.assertEqual(value, 'foo')
        self.assertEqual(mock_pool._available_connections, [conn_1, conn_3, conn_2])
