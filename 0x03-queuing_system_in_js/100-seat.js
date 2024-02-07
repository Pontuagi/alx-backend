const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis Client Setup
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function reserveSeat (number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats () {
  const seats = await getAsync('available_seats');
  return parseInt(seats) || 0;
}

// Initialize available seats to 50
reserveSeat(50);

// Initialize reservation status
let reservationEnabled = true;

// Kue Queue Setup
const queue = kue.createQueue();

// Express Server Setup
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

// Routes
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();
    if (currentAvailableSeats === 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else if (currentAvailableSeats > 0) {
      await reserveSeat(currentAvailableSeats - 1);
      if (currentAvailableSeats - 1 === 0) {
        reservationEnabled = false;
      }
      done();
    }
  });
});

// Queue Events
queue.on('job complete', (id) => {
  console.log(`Seat reservation job ${id} completed`);
});

queue.on('job failed', (id, err) => {
  console.log(`Seat reservation job ${id} failed: ${err}`);
});
