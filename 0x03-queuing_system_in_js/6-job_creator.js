import kue from 'kue';

const queue = kue.createQueue();

const job = {
  phoneNumber: '09056333625',
  message: 'How do you do?'
};
const notificationJob = queue.create('push_notification_code', job);
notificationJob.on('enqueue', () => console.log(`Notification job created: ${notificationJob.id}`));
notificationJob.on('complete', () => console.log('Notification job completed'));
notificationJob.on('failed', (err) => console.error('Notification job failed: ', err));
notificationJob.save();
