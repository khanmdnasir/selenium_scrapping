import pika
from bots import BaseBot
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',heartbeat=5000))
channel = connection.channel()

channel.queue_declare(queue='update_queue')

def callback(ch, method, properties, body):
    print(body)
    try:
        bot = BaseBot()
        bot.update()
    except Exception as e:
        print(str(e))

channel.basic_consume(queue='update_queue', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
