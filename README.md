testing flask app with gunicorn nginx jenkins


directory=/var/lib/jenkins/workspace/test-flask
command=/var/lib/jenkins/workspace/test-flask/venv/bin/gunicorn manager:create_app -b localhost:8000
autostart=true
autorestart=true
stderr_logfile=/var/log/test_flask/application.err.log
stdout_logfile=/var/log/test_flask/application.out.log
