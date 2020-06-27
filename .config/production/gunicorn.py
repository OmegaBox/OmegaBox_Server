daemon = False
chdir = '/srv/omegabox/app'
bind = 'unix:/run/omegabox.sock'
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
capture_output = True
