const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

const queue = kue.createQueue();

const initialSeats = 50;
let reservationEnabled = true;

setAsync('available_seats', initialSeats);

async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10) || 0;
}

app.get('/available_seats', async (req, res) => {
  try {
    const seats = await getCurrentAvailableSeats();
    res.json({ available_seats: seats });
  } catch (err) {
    res.status(500).json({ error: 'Failed to retrieve available seats' });
  }
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  const job = queue.create('reserve_seat').save(err => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

queue.process('reserve_seat', async (job, done) => {
  try {
    const currentSeats = await getCurrentAvailableSeats();
    if (currentSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }
    await reserveSeat(currentSeats - 1);
    done();
  } catch (err) {
    done(err);
  }
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentSeats = await getCurrentAvailableSeats();
      if (currentSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }
      await reserveSeat(currentSeats - 1);
      console.log(`Seat reservation job ${job.id} completed`);
      done();
    } catch (err) {
      console.error(`Seat reservation job ${job.id} failed: ${err.message}`);
      done(err);
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

