import os
import logging
import argparse

from dotenv import load_dotenv

from server import TestCheckerServer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka_broker_addr", type=str, default=os.getenv("KAFKA_BROKER_ADDR"))
    parser.add_argument("--kafka_broker_port", type=int, default=os.getenv("KAFKA_BROKER_PORT"))
    parser.add_argument("--kafka_request_topic", type=str, default=os.getenv("KAFKA_REQUEST_TOPIC"))
    parser.add_argument("--kafka_response_topic", type=str, default=os.getenv("KAFKA_RESPONSE_TOPIC"))
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(levelname)s][%(filename)s] %(message)s",
        datefmt="%H:%M:%S %d-%m-%Y",
    )

    server: TestCheckerServer = TestCheckerServer(
        kafka_broker_addr=args.kafka_broker_addr,
        kafka_broker_port=args.kafka_broker_port,
        kafka_request_topic=args.kafka_request_topic,
        kafka_response_topic=args.kafka_response_topic,
    )
    server.run()


if __name__ == "__main__":
    load_dotenv()
    main(parse_args())
