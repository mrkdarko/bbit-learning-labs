#!/usr/bin/env python

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

import os
import sys
from pathlib import Path

import pika

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from consumer_interface import mqConsumerInterface


class mqConsumer(mqConsumerInterface):
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        """
        Initialize the consumer with binding key, exchange name, and queue name for topic exchange.
        
        Args:
            binding_key: The topic binding pattern (e.g., stock.*.tech)
            exchange_name: The name of the topic exchange to bind to
            queue_name: The name of the queue to create and bind
        """
        # Save parameters to class variables
        self.binding_key = binding_key
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.connection = None
        self.channel = None
        
        # Call setupRMQConnection
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        """
        Set up connection to RabbitMQ service.
        Establishes channel, creates topic exchange, queue, and binding.
        """
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)

        # Establish Channel
        self.channel = self.connection.channel()

        # Create the topic exchange if not already present
        self.channel.exchange_declare(
            exchange=self.exchange_name, 
            exchange_type="topic", 
            durable=False
        )

        # Create Queue if not already present
        self.channel.queue_declare(queue=self.queue_name, durable=False)

        # Bind Binding Key to Queue on the exchange with topic pattern
        self.channel.queue_bind(
            queue=self.queue_name,
            routing_key=self.binding_key,
            exchange=self.exchange_name,
        )

        # Set-up Callback function for receiving messages
        self.channel.basic_consume(
            self.queue_name, self.on_message_callback, auto_ack=False
        )

    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        """
        Handle incoming messages from the queue.
        
        Args:
            channel: The channel on which the message arrived
            method_frame: Frame containing delivery information
            header_frame: Frame containing headers
            body: The message body
        """
        # Acknowledge Message 
        channel.basic_ack(method_frame.delivery_tag, False)

        # Decode and print message
        message = body.decode('utf-8')
        routing_key = method_frame.routing_key
        print(f"[Consumer] Received message on routing key '{routing_key}': {message}")

       
    def startConsuming(self) -> None:
        """
        Start consuming messages from the queue.
        """
        # Print waiting message with binding key pattern
        print(f" [*] Waiting for messages with pattern '{self.binding_key}'. To exit press CTRL+C")

        # Start consuming messages
        self.channel.start_consuming()

    def __del__(self) -> None:
        """Clean up connection on deletion."""
        if hasattr(self, 'channel') and self.channel:
            self.channel.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
