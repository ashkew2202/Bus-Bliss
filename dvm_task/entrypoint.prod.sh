if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $PORT_NUMBER; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"