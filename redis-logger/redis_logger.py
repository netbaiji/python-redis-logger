import redis
import json


class RedisLogger():
    def __init__(self, host="localhost", port=6379, channel="test"):
        self.client = redis.StrictRedis(host=host, port=port)
        self.channel = channel

    def log(self, log_type, filename, message):
        _log = {
            'filename': filename,
            'message': message
        }

        self.client.lpush(
            "%s__%s" % (self.channel, log_type),
            json.dumps(_log)
        )

    def error(self, filename, message):
        self.log("error", filename, message)

    def fatal(self, filename, message):
        self.log("fatal", filename, message)

    def warning(self, filename, message):
        self.log("warning", filename, message)

    def debug(self, filename, message):
        self.log("debug", filename, message)

    def info(self, filename, message):
        self.log("info", filename, message)

    # Getting logs
    def get(self, log_type, range_from, range_to):
        channel = "%s__%s" % (self.channel, log_type)

        size = self.client.llen(channel)
        first, last = size - range_to, size - range_from

        print first, last

        return self.client.lrange(channel, first, last)

    def get_last_errors(self, range_from, range_to):
        return self.get("error", range_from, range_to)

"""
if __name__ == "__main__":
    logger = RedisLogger()

    logger.error("redis_logger.py", "Test message")

    # get last 3 errors

    print logger.get_last_errors(1, 3)
"""
