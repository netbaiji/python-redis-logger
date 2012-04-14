import redis
import json
import datetime
import inspect

# Get file and line_no where logger was called
# First three entries are from this library, skip them
def get_traceback():
    frame, filename, line_no = inspect.stack()[3][:3]
    return "%s:%s" % (filename, line_no)


class RedisLogger():
    def __init__(self, host="localhost", port=6379, channel="test"):
        self.client = redis.StrictRedis(host=host, port=port)
        self.channel = channel

    def log(self, log_type, message, filename=None):
        _log = {
            'filename': filename or get_traceback(),
            'message': message,
            'pubdate': str(datetime.datetime.now()),
        }

        # Send log to Redis
        try:
            self.client.lpush(
                "%s__%s" % (self.channel, log_type),
                json.dumps(_log)
            )
        except redis.exceptions.ConnectionError:
            pass

        # If Pusher client is attached also log into it
        if hasattr(self, "pusher_client") \
          and getattr(self, "pusher_client") is not None:
            _log["type"] = log_type
            _log["channel"] = self.channel

            self.pusher_client["logs"].trigger(
                "log_entry_created",
                {'entry': json.dumps(_log)}
            )

    # Sets channel (if you want to change redis channel,
    #   but you don't want to reset connection)
    def set_channel(self, channel):
        self.channel = channel

    # Attach pusher client, if you want to push notifications about
    #   logs on pusher.com (realtime logging)
    def attach_pusher_client(self, pusher_client):
        self.pusher_client = pusher_client

    def error(self, message, filename=None):
        self.log("error", message, filename)

    def fatal(self, message, filename=None):
        self.log("fatal", message, filename)

    def warning(self, message, filename=None):
        self.log("warning", message, filename)

    def debug(self, message, filename=None):
        self.log("debug", message, filename)

    def info(self, message, filename=None):
        self.log("info", message, filename)

    # Getting logs
    def get(self, log_type, range_from, range_to):
        channel = "%s__%s" % (self.channel, log_type)

        size = self.client.llen(channel)
        #first, last = size - range_to, size - range_from
        first, last = range_from - 1, range_to - 1

        return self.client.lrange(channel, first, last)

    def get_last_errors(self, range_from, range_to):
        return self.get("error", range_from, range_to)

    def get_last_fatals(self, range_from, range_to):
        return self.get("fatal", range_from, range_to)

    def get_last_warnings(self, range_from, range_to):
        return self.get("warning", range_from, range_to)

    def get_last_debugs(self, range_from, range_to):
        return self.get("debug", range_from, range_to)

    def get_last_infos(self, range_from, range_to):
        return self.get("info", range_from, range_to)


if __name__ == "__main__":
    logger = RedisLogger(channel="development")

    # create pusher client
    import pusher
    p = pusher.Pusher(
        app_id = 'your-app-id',
        key = 'your-key',
        secret = 'your-secret-key'
    )

    logger.attach_pusher_client(p)
