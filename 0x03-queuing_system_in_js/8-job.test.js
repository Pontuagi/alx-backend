const kue = require('kue');
const { expect } = require('chai');
const createPushNotificationsJobs = require('./8-job');

/* global describe, beforeEach, afterEach, it */

describe('createPushNotificationsJobs', () => {
  let queue;

  // Set up the Kue queue and enter test mode
  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  // Clear the queue and exit test mode after each test
  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => {
      createPushNotificationsJobs('not an array', queue);
    }).toThrowError('Jobs is not an array');
  });

  it('should create a job for each job object in the array', () => {
    const jobs = [
      { phoneNumber: '123', message: 'Message 1' },
      { phoneNumber: '456', message: 'Message 2' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Verify that the correct number of jobs is created in the queue
    expect(queue.testMode.jobs.length).toBe(jobs.length);
  });

  it('should log messages when jobs are created, completed, failed, and making progress', () => {
    const jobs = [
      { phoneNumber: '123', message: 'Message 1' },
      { phoneNumber: '456', message: 'Message 2' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Iterate over each job to verify log messages
    jobs.forEach((jobData) => {
      const job = queue.testMode.jobs.find(j => j.type === 'push_notification_code_3' && j.data.phoneNumber === jobData.phoneNumber);

      expect(job.log).toContain(`Notification job created: ${job.id}`);

      job.emit('complete');
      expect(job.log).toContain(`Notification job ${job.id} completed`);

      job.emit('failed', new Error('Some error'));
      expect(job.log).toContain(`Notification job ${job.id} failed: Error: Some error`);

      job.emit('progress', 50);
      expect(job.log).toContain(`Notification job ${job.id} 50% complete`);
    });
  });
});
