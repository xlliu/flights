from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue

q = Queue(maxsize=2)

@gen.coroutine
def consumer():
    while True:
        print '0'
        item = yield q.get()
        print '2'
        try:
            print('Doing work on %s' % item)
            yield gen.sleep(0.01)
        finally:
            q.task_done()
            print('111')

@gen.coroutine
def producer():
    for item in range(5):
        yield q.put(item)
        print('Put %s' % item)

@gen.coroutine
def main():
    # Start consumer without waiting (since it never finishes).
    IOLoop.current().spawn_callback(consumer)
    yield producer()     # Wait for producer to put all tasks.
    yield q.join()       # Wait for consumer to finish all tasks.
    print('Done')

IOLoop.current().run_sync(main)
