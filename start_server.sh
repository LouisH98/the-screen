nohup gunicorn -w 1 --worker-connections 1 -b 0.0.0.0 -k uvicorn.workers.UvicornWorker --threads 6 main:app &
