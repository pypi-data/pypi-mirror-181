from time import sleep
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.python import log

from txamqp.protocol import AMQClient
from txamqp.client import TwistedDelegate

import txamqp.spec
import pkg_resources

from .sources import MongoDB
import logging


script_log = "bill-> "


@inlineCallbacks
def gotConnection(conn, username, password):
    print(f"{f'{script_log}*** Connected to broker, authenticating: {username}':<65}"+"***", flush=True)
    yield conn.authenticate(username, password)

    print(f"{f'{script_log}*** Authenticated. Ready to receive messages':<65}"+"***", flush=True)
    print(f"{f'{script_log}***':<65}"+"***", flush=True)
    chan = yield conn.channel(1)
    yield chan.channel_open()

    yield chan.queue_declare(queue="billingQueue")

    # Bind to routes
    yield chan.queue_bind(queue="billingQueue", exchange="billing", routing_key='bill_request.submit_sm_resp.*')

    yield chan.basic_consume(queue='billingQueue', no_ack=True, consumer_tag="billingFollower")
    queue = yield conn.queue("billingFollower")

    if config_ready is not True:
        return

    mongosource = MongoDB(
        database_name=MONGODB_BILL_DATABASE, script_log=script_log)

    if mongosource.startConnection() is not True:
        return

    # Wait for messages
    # This can be done through a callback ...
    while True:
        msg = yield queue.get()
        bill = msg.content.properties['headers']
        mongosource.increment_one(
            module=MONGODB_BILL_COLLECTION,
            sub_id=bill['user-id'],
            data={
                MONGODB_BILL_BALANCE_KEY: bill['amount']
            }
        )

    # A clean way to tear down and stop
    yield chan.basic_cancel("billingFollower")
    yield chan.channel_close()
    chan0 = yield conn.channel(0)
    yield chan0.connection_close()

    reactor.stop()


def rabbitMQConnect():
    host = amqp_broker_host
    port = amqp_broker_port
    vhost = '/'
    username = 'guest'
    password = 'guest'
    spec_file = pkg_resources.resource_filename('jasmin_realtime', 'amqp0-9-1.xml')

    spec = txamqp.spec.load(spec_file)

    def whoops(err):
        print(
            f"{f'{script_log}*** Error connecting to RabbitMQ server.':<65}"+"***", flush=True)
        print(f"{f'{script_log}*** Shutting down !!!':<65}"+"***", flush=True)
        print(f"{f'{script_log}*':*<68}", flush=True)
        if reactor.running:
            log.err(err)
            reactor.stop()
        sleep(3)

    try:
        # Connect and authenticate
        d = ClientCreator(reactor,
                          AMQClient,
                          delegate=TwistedDelegate(),
                          vhost=vhost,
                          spec=spec).connectTCP(host, port)
        d.addCallback(gotConnection, username, password)

        d.addErrback(whoops)

        reactor.run()
    except Exception as err:
        print(
            f"{f'{script_log}*** Error connecting to RabbitMQ server.':<65}"+"***", flush=True)
        print(f"{f'{script_log}*** Shutting down !!!':<65}"+"***", flush=True)
        print(f"{f'{script_log}*':*<68}", flush=True)


if __name__ == "__main__":
    print(" ", flush=True)
    print(" ", flush=True)
    print(f"{f'{script_log}*************** `Bill watcher` ':*<68}", flush=True)
    print(f"{f'{script_log}***         Staring `Bill watcher`':<65}"+"***", flush=True)
    print(f"{f'{script_log}*':*<68}", flush=True)

    print(f"{f'{script_log}*** Checking MongoDB connection settings...':<65}"+"***", flush=True)
    if config_ready is not True:
        print(
            f"{f'{script_log}*** no MongoDB configurations found!':<65}"+"***", flush=True)
        print(f"{f'{script_log}*** Shutting down !!!':<65}"+"***", flush=True)
        print(f"{f'{script_log}*':*<68}", flush=True)
        exit()

    print(f"{f'{script_log}*** MongoDB READY!':<65}"+"***", flush=True)
    print(f"{f'{script_log}*** Set to use MongoDB connection':<65}" +
          "***", flush=True)
    print(f"{f'{script_log}*** ':<65}"+"***", flush=True)
    rabbitMQConnect()
