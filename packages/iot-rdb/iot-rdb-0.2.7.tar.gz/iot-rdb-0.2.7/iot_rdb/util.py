from redis.exceptions import ConnectionError
from threading import Thread
try:
    import queue
except ImportError:
    import Queue as queue
import redis
import time
import json


class IotRedisBasic(object):
    """Basic redis variable to set and retrieve data

    Base class for Redis variable"""

    def __init__(self):
        super(IotRedisBasic, self).__init__()
        self.rdb = redis.Redis(
            host='localhost',
            port=6379,
            charset="utf-8",
            decode_responses=True,
            db=0
        )

    def get(self, var):
        # type: (str) -> None

        try:
            return self.rdb.get(var)
        except ConnectionError as _:
            return

    def set(self, var_name, value):
        # type: (str, dict) -> None

        try:
            if not isinstance(value, dict):
                raise TypeError()
            self.rdb.set(var_name, json.dumps(value))
        except ConnectionError as _:
            print("ConnetionError trying to set var")
        except TypeError as _:
            print("Value has to be a dictionary")


class IotRedisSubscriber(IotRedisBasic, Thread):
    """Class for consume info, inherits from Thread

    This class provides basic connetion to redis and consumes
    a list of channels to subscribe when is started.
    func_handler can be parsed to develop async distribution of data
    to a custom function.
    """

    def __init__(self, *channels_to_consume, **kwargs):
        # type: (*str, any) -> None

        super(IotRedisSubscriber, self).__init__()
        self.daemon = True
        self.data_list = queue.Queue()
        self.init_channels = list(channels_to_consume)
        if 'func_handler' in kwargs:
            self.func_handler = kwargs.pop('func_handler')
        else:
            self.func_handler = None
        # Create pubsub instance for subscribe
        self.pubsub = self.rdb.pubsub(ignore_subscribe_messages=True)

    @property
    def channels(self):
        return self.pubsub.channels

    def run(self):
        # type () -> None

        # Subscribe
        self._subscribe_channels(*self.init_channels)
        while True:
            try:
                self.pubsub.ping()
                self.listen()
            except ConnectionError as err:
                print("Problem trying to listen, relisten...")
                print(f"Err: {err}")
            except AttributeError as _:
                print("None type of msg")
            finally:
                time.sleep(0.5)

    def listen(self):
        # type: () -> None

        for msg in self.pubsub.listen():
            if msg is not None and isinstance(msg, dict):
                # Save info in queue.
                data = self._convert_data(msg['data'])
                if self.func_handler is not None:
                    self.func_handler((msg['channel'], data))
                else:
                    self.data_list.put((msg['channel'], data))

    def _convert_data(self, data):
        # type: (str) -> any

        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            return data
        except TypeError:
            return data

    def _subscribe_channels(self, *channels_to_consume):
        # type: (*str) -> None

        while True:
            try:  # Suscribe to every channel
                self.pubsub.subscribe(*channels_to_consume)
            except ConnectionError as err:
                print("Error trying to connect to server:", err)
                time.sleep(1)
            else:  # If no error
                break

    def unsubscribe_channels(self, *channels_to_unsubscribe):
        # type: (*str) -> None

        try:
            self.pubsub.unsubscribe(channels_to_unsubscribe)
        except ConnectionError as err:
            print("Error trying to unsusbscribe to server:", err)
            time.sleep(1)

    def data_available(self):
        # type: () -> bool

        return not self.data_list.empty()

    def retrieve_data(self):
        # type: () -> tuple

        try:
            return self.data_list.get_nowait()
        except queue.Empty as _:
            return


class IotRedisPublisher(IotRedisBasic):
    def __init__(self, *args, **kwargs):
        super(IotRedisPublisher, self).__init__(*args, **kwargs)

    def publish(self, channel, data):
        # type: (str, dict) -> None

        try:  # Publish data to channel
            if not isinstance(data, dict):
                raise TypeError("Type has to be a dictionary")
            return self.rdb.publish(channel, json.dumps(data))
        except ConnectionError as _:
            print("error trying to publish")


class IotRedisPubSub(IotRedisPublisher, IotRedisSubscriber):
    def __init__(self, *args, **kwargs):
        super(IotRedisPubSub, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    pubsub = IotRedisPubSub("hola", "opcua")
    print(pubsub.channels)
    sample_consumer = IotRedisSubscriber('prueba1', 'prueba2')
    sample_consumer.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt as _:
            break
    print("Simulation ended")
