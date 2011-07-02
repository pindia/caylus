import logging

class MessageQueue(object):
    
    queues = {}
    
    @staticmethod
    def get_queue(id):
        if id in MessageQueue.queues:
            return MessageQueue.queues[id]
        else:
            queue = MessageQueue(id)
            MessageQueue.queues[id] = queue
            return queue
        
    @staticmethod
    def delete_queue(id):
        if id in MessageQueue.queues:
            del MessageQueue.queues[id]
    
    
    def __init__(self, id):
        self.id = id
        self.waiters = []
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, callback, cursor=None, id=None):
        if cursor:
            index = 0
            for i in xrange(len(self.cache)):
                index = len(self.cache) - i - 1
                if self.cache[index]["id"] == cursor: break
            recent = self.cache[index + 1:]
            if recent:
                callback(recent)
                return
        self.waiters.append(callback)

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for callback in self.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]