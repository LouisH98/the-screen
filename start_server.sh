nohup gunicorn -w 1 -b 0.0.0.0 -k uvicorn.workers.UvicornWorker main:app &
