# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

#copy file media
python manage.py copy_media

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Apply database migrations
#echo "Seed data from fixtures"
#python manage.py loaddata fixtures/categories.json
#python manage.py loaddata fixtures/classification.json

echo "start server"
uwsgi --ini sakura_housing_uwsgi.ini