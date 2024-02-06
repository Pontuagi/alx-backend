import redis from 'redis';
import { promisify } from 'util';

// Create a Redis client
const client = redis.createClient();

// Event listeners for client connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err}`);
});

// Promisify redis functions
const getAsync = promisify(client.get).bind(client);

// Function to set a new school value
function setNewSchool (schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Display value for a given school name
async function displaySchoolValue (schoolName) {
  try {
    const reply = await getAsync(schoolName);
    console.log(`${reply}`);
  } catch (err) {
    console.error(`Error retrieving value for ${schoolName}: ${err}`);
  }
}

// Call the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
