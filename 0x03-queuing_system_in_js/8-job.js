const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) throw Error('Jobs is not an array');
  for (const job of jobs) {
    const newJob = queue.createJob('push_notification_code_3', job);
    newJob.on('enqueue', () => console.log(`Notification job created: ${newJob.id}`));
    newJob.on('complete', () => console.log(`Notification job ${newJob.id} completed`));
    newJob.on('failed', (err) => console.log(`Notification job ${newJob.id} failed: ${err}`));
    newJob.on('progress', (progress) => console.log(`Notification job ${newJob.id} ${progress}% complete`));
    newJob.save();
  }
};

module.exports = createPushNotificationsJobs;
