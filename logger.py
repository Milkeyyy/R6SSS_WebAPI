import logging
import logging.handlers


logger = logging.getLogger("r6sss")
logger.setLevel(logging.INFO)

#stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s [%(thread)d] %(message)s")
#stream_handler.setFormatter(stream_formatter)
#logger.addHandler(stream_handler)

rotating_handler = logging.handlers.RotatingFileHandler(
	r'./app.log',
	mode="a",
	maxBytes=100 * 1024,
	backupCount=3,
	encoding="utf-8"
)
rotating_handler.setLevel(logging.INFO)
rotating_handler.setFormatter(stream_formatter)
logger.addHandler(rotating_handler)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.addHandler(rotating_handler)
for _f in uvicorn_logger.handlers:
	_f.setFormatter(stream_formatter)
