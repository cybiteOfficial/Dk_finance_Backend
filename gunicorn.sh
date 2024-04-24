#!/bin/bash
   # Activate your virtual environment (if applicable)
   source /home/ubuntu/Dk_finance_Backend/venv/bin/activate
   # Navigate to your Django project directory
   cd /home/ubuntu/Dk_finance_Backend
   # Start Gunicorn with your Django project
   gunicorn Dev_Kripa_Finance.wsgi:application --bind 0.0.0.0:5000 --timeout 300
