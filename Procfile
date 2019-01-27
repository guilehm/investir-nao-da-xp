web: gunicorn xp.wsgi --log-file -
celery: celery worker -A xp -l info
bot: python -m bot.clients.discord
