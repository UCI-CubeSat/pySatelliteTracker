import subprocess
from pymemcache.client.base import Client

subprocess.run(["brew", "services", "start", "memcached"])
client = Client('localhost')
client.timeout = 1
client.connect_timeout = 5
client.set('some_key', 'some_value')
result = client.get('some_key')
print(result)
