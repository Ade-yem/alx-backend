// 1-redis_op.js

import { createClient, print } from 'redis';
import { promisify } from 'util';

// Create a Redis client instance connecting to localhost
const client = createClient({});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (error) => {
  console.error('Redis client not connected to the server:', error);
});
const get = promisify(client.get).bind(client);

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, print);
};
const displaySchoolValue = async (schoolName) => {
  await get(schoolName)
    .then((res) => console.log(res)).catch(err => console.log(err));
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
