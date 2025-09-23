from config import Config
from processing import PaymentProcessor
from loguru import logger
import argparse
import sys

logger.remove()

logger.add(
    "errors.log",
    level="ERROR",
    format="{time} | Line {extra[line]}: {message}",
    enqueue=True,
    backtrace=True,
    diagnose=False
)

logger.add(
    "progress.log",
    level="INFO",
    format="{time} | {message}",
    filter=lambda record: record["level"].name == "INFO",
    enqueue=True
)

logger.add(
    sys.stdout,
    level="INFO",
    format="{message}",
    filter=lambda record: record["level"].name == "INFO"
)

parser = argparse.ArgumentParser(description="Process payments CSV in chunks.")
parser.add_argument("--input", required=True)
parser.add_argument("--chunk-size", type=int, default=10000)
parser.add_argument("--output-aggregates", required=True)
parser.add_argument("--offset-file", required=True)
args = parser.parse_args()

config = Config(
    input_file=args.input,
    output_file=args.output_aggregates,
    offset_file=args.offset_file,
    chunk_size=args.chunk_size,
)
processor = PaymentProcessor(config)
processor.process()
