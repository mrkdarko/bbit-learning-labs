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

from solution.consumer_sol import mqConsumer  # pylint: disable=import-error

def main(sector: str, queueName: str) -> None:
    
    # Create Binding Key from the sector variable - Step 2
    # Format: stock.*.SECTOR matches all messages for that sector
    binding_key = f"stock.*.{sector}"
    
    consumer = mqConsumer(
        binding_key=binding_key,
        exchange_name="Tech Lab Topic Exchange",
        queue_name=queueName
    )    
    consumer.startConsuming()
    


if __name__ == "__main__":

    # Implement Logic to read the sector and queueName string from the command line and save them - Step 1
    parser = argparse.ArgumentParser(
        description="Process Sector and Queue Name."
    )
    parser.add_argument(
        "sector",
        metavar="sector",
        type=str,
        help="The sector to subscribe to (e.g., tech, healthcare)"
    )
    parser.add_argument(
        "queueName",
        metavar="queueName", 
        type=str,
        help="The name of the queue"
    )
    
    args = parser.parse_args()
    sector = args.sector
    queueName = args.queueName

    sys.exit(main(sector, queueName))
