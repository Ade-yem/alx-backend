// 0-redis_op.js

import { createClient } from "redis";

// Create a Redis client instance connecting to localhost
const client = createClient({});

client.on("connect", () => {
  console.log('Redis client connected to the server');
});

client.on("error", (error) => {
  console.error('Redis client not connected to the server:', error);
});
