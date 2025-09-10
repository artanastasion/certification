from config import Config
from processing import PaymentProcessor

import argparse

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
