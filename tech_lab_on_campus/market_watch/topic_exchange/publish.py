# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys

from solution.producer_sol import mqProducer  # pylint: disable=import-error


def main(ticker: str, price: float, sector: str) -> None:
    
    # Create Routing Key from the ticker and sector variable - Step 2
    # Format: stock.TICKER.SECTOR
    routing_key = f"stock.{ticker}.{sector}"

    producer = mqProducer(routing_key=routing_key, exchange_name="Tech Lab Topic Exchange")

    # Create a message variable from the variables EG. "TSLA price is now $500" - Step 3
    message = f"{ticker} is ${price}"
    
    producer.publishOrder(message)


if __name__ == "__main__":

    # Read the ticker, price and sector string from the command line and save them - Step 1
    parser = argparse.ArgumentParser(description='Publish stock price updates to RabbitMQ topic exchange')
    parser.add_argument('ticker', type=str, help='Stock ticker symbol (e.g., TSLA)')
    parser.add_argument('price', type=float, help='Stock price (e.g., 182.34)')
    parser.add_argument('sector', type=str, help='Industry sector (e.g., tech, healthcare)')
    
    args = parser.parse_args()

    sys.exit(main(args.ticker, args.price, args.sector))
