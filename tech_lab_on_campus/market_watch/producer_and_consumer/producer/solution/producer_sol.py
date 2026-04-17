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
from producer_interface import mqProducerInterface


class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        """
        Initialize the producer with routing key and exchange name.
        
        Args:
            routing_key: The routing key for messages
            exchange_name: The name of the exchange to publish to
        """
        # Save parameters to class variables
        # self.routing_key = routing_key
        # self.exchange_name = exchange_name
        
        # Call setupRMQConnection
        # self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        """
        Set up connection to RabbitMQ service.
        Establishes channel and creates exchange if not present.
        """
        # Set-up Connection to RabbitMQ service
        # con_params = pika.URLParameters(os.environ["AMQP_URL"])
        # self.connection = pika.BlockingConnection(parameters=con_params)
        
        # Establish Channel
        # self.channel = self.connection.channel()
        
        # Create the exchange if not already present
        # self.channel.exchange_declare(exchange=self.exchange_name)

    def publishOrder(self, message: str) -> None:
        """
        Publish a message to the exchange using the routing key.
        
        Args:
            message: The message string to publish
        """
        # Basic Publish to Exchange
        # self.channel.basic_publish(
        #     exchange=self.exchange_name,
        #     routing_key=self.routing_key,
        #     body=message,
        # )
        
        # Close Channel
        # self.channel.close()
        
        # Close Connection
        # self.connection.close()
