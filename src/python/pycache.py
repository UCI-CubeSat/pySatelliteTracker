from pymemcache.client.base import Client

# brew services start memcached
client = Client('localhost')
client.set('key', 'value')
result = client.get('key')
print(result)
