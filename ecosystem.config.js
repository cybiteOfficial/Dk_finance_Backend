module.exports = {
  apps: [
    {
      name: 'my-django-app',
      script: 'gunicorn',
      args: 'Dev_Kripa_Finance.wsgi:application --bind 0.0.0.0:5000',
      exec_mode: 'fork', // or 'cluster'
      instances: 1, // Change for more instances
      watch: false, // Enable to automatically restart on changes
      autorestart: true,
      max_memory_restart: '1G',
    },
  ],
};
