import { createClient } from 'redis';
import kue from 'kue';
import { promisify } from 'util';
const express = require('express');

const app = express();
const client = createClient();
const queue = kue.createQueue();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (error) => {
  console.error('Redis client not connected to the server:', error);
});

const number = 50;
let reservationEnabled = true;
const reserveSeat = (number) => client.set('available_seats', number);

const getCurrentAvailableSeats = async () => {
  const getAsync = promisify(client.get).bind(client);
  const res = await getAsync('available_seats');
  if (res === 0) reservationEnabled = false;
  return res;
};

reserveSeat(number);
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  return res.json({ available_seats: availableSeats });
});
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) return res.json({ status: 'Reservation are blocked' });
  const job = queue.createJob('reserve_seat').save(err => {
    if (!err) return res.json({ status: 'Reservation in process' });
    else return res.json({ status: 'Reservation failed' });
  }).on('failed', (err) => console.log(`Seat reservation job ${job.id} failed: ${err}`))
    .on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });
  const available = await getCurrentAvailableSeats();
  if (available > 0) {
    queue.process('reserve_seat', async (job, done) => {
      try {
        const availableSeats = await getCurrentAvailableSeats();
        if (availableSeats <= 0) {
          reservationEnabled = false;
          return done(new Error('No seats available'));
        }
        await reserveSeat(availableSeats - 1);
        if (availableSeats - 1 === 0) {
          reservationEnabled = false;
        }
        done();
      } catch (error) {
        done(error);
      }
    });
  }
});

app.listen(1245, () => { console.log('Server is listening on port 1245'); });
