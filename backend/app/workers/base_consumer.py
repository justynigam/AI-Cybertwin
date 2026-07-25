import redis
import time
import json
import logging

class RedisStreamConsumer:
    def __init__(self, redis_url: str, stream_name: str, group_name: str, consumer_name: str):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.stream_name = stream_name
        self.group_name = group_name
        self.consumer_name = consumer_name
        
        # Ensure the consumer group exists, create if not
        try:
            self.redis.xgroup_create(self.stream_name, self.group_name, id='0', mkstream=True)
            logging.info(f"Created Consumer Group {self.group_name} on {self.stream_name}")
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                pass # Group already exists
            else:
                raise e

    def listen(self, process_callback):
        """
        Blocking loop that listens for new messages in the stream.
        """
        logging.info(f"Consumer {self.consumer_name} listening to {self.stream_name}...")
        
        while True:
            try:
                # 1. Read from the stream (Block for 2 seconds waiting for new messages)
                # '>' means read new messages not yet delivered to other consumers in the group
                messages = self.redis.xreadgroup(
                    groupname=self.group_name,
                    consumername=self.consumer_name,
                    streams={self.stream_name: '>'},
                    count=10,
                    block=2000 
                )

                if not messages:
                    continue # No new messages, loop again

                # 2. Process messages
                for stream, msg_list in messages:
                    for message_id, payload in msg_list:
                        # Extract the actual JSON data
                        raw_data = payload.get('data')
                        if raw_data:
                            event_dict = json.loads(raw_data)
                            
                            # 3. Execute the business logic (ML Inference, etc.)
                            success = process_callback(event_dict)
                            
                            # 4. Acknowledge (ACK) the message if successful
                            # This tells Redis the message is done and can be removed from pending
                            if success:
                                self.redis.xack(self.stream_name, self.group_name, message_id)
                                
            except Exception as e:
                logging.error(f"Stream processing error: {str(e)}")
                time.sleep(1) # Backoff before retrying
