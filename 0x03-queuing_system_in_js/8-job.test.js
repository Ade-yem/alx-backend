const kue = require('kue');
const createPushNotificationsJobs = require('./8-job.js');
const { expect } = require('chai');

const queue = kue.createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account'
  }
];

describe('createPushNotificationsJobs', () => {
  before(() => queue.testMode.enter());
  afterEach(() => queue.testMode.clear());
  after(() => queue.testMode.exit());

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw(Error);
  });

  it('should create new jobs in the queue', () => {
    createPushNotificationsJobs(jobs, queue);

    const jobsInQueue = queue.testMode.jobs;
    expect(jobsInQueue.length).to.equal(3);
    let i = 0;
    for (const job of jobsInQueue) {
      expect(job.type).to.equal('push_notification_code_3');
      expect(job.data).to.eql(jobs[i]);
      i += 1;
    }
  });
});
