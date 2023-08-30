// 1-redis_op.js

import { createClient, print } from 'redis';

// Create a Redis client instance connecting to localhost
const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (error) => {
  console.error('Redis client not connected to the server:', error);
});

const value = {
  Portland: 50, Seattle: 80, 'New York': 20, Bogota: 20, Cali: 40, Paris: 2
};

for (const key in value) {
  client.hset('HolbertonSchools', key, value[key], print);
}
client.hgetall('HolbertonSchools', (err, res) => {
  if (err) console.log(err);
  else console.log(res);
});
