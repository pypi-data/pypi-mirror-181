import contextlib
import time


@contextlib.contextmanager
def timer(logger, prefix: str):
    start_time = time.time()
    logger.info(f"Starting {prefix}")
    yield
    logger.info(f"Finished {prefix} took {time.time() - start_time:.2f} [s]")
