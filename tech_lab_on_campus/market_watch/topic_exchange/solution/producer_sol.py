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

import pika
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from producer_interface import mqProducerInterface


class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        """
        Initialize the producer with routing key and exchange name for topic exchange.
        
        Args:
            routing_key: The topic routing key for messages (e.g., stock.TSLA.tech)
            exchange_name: The name of the topic exchange to publish to
        """
        # Save parameters to class variables
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        
        # Call setupRMQConnection
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        """
        Set up connection to RabbitMQ service.
        Establishes channel and creates topic exchange if not present.
        """
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        
        # Establish Channel
        self.channel = self.connection.channel()
        
        # Create the topic exchange if not already present
        self.channel.exchange_declare(
            exchange=self.exchange_name, 
            exchange_type='topic', 
            durable=False
        )

    def publishOrder(self, message: str) -> None:
        """
        Publish a message to the topic exchange using the routing key.
        
        Args:
            message: The message string to publish
        """
        # Basic Publish to Exchange
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message.encode('utf-8'),
        )
        
        print(f"[Producer] Published message with routing key '{self.routing_key}': {message}")
        
        # Give RabbitMQ a moment to route the message
        import time
        time.sleep(0.1)
        
        # Close Channel
        self.channel.close()
        
        # Close Connection
        self.connection.close()
