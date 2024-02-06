const kue = require('kue');
const queue = kue.createQueue();

// Function to send notification
function sendNotification (phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Process jobs from push_notification_code
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done();
});

// Event listener for queue errors
queue.on('error', (err) => {
  console.error('Queue error:', err);
});
