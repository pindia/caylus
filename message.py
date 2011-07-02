import logging

class MessageMixin(object):
    waiters = []
    waiter_ids = []
    cache = []
    cache_size = 200

    def wait_for_messages(self, callback, cursor=None, id=None):
        cls = MessageMixin
        if cursor:
            index = 0
            for i in xrange(len(cls.cache)):
                index = len(cls.cache) - i - 1
                if cls.cache[index]["id"] == cursor: break
            recent = cls.cache[index + 1:]
            if recent:
                ms = [m for m in recent if m.id == id]
                if ms:
                    callback(ms)
                    return
        cls.waiters.append(callback)
        cls.waiter_ids.append(id)

    def new_messages(self, messages):
        cls = MessageMixin
        logging.info("Sending new message to %r listeners", len(cls.waiters))
        for callback, id in zip(cls.waiters, cls.waiter_ids):
            try:
                ms = [m.data for m in messages if m.id == id]
                if ms:
                    callback(ms)
                    i = cls.waiters.index(callback)
                    del cls.waiters[i]
                    del cls.waiter_ids[i]
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.cache.extend(messages)
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]