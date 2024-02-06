import redis from 'redis';

// create redis client
const client = redis.createClient();

//Event listeners for client connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});


client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});
