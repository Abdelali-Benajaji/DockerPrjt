import pika, json

def microservice_send():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='send_queue')
    channel.queue_declare(queue='auth_demande')
    channel.queue_declare(queue='auth_reponse')


    code = input("Entrer le code : ")
    channel.basic_publish(exchange='', routing_key='auth_demande', body=code)

    def callback(ch, method, properties, body):
        body = body.decode('utf-8')
        if body == 'oui':
            with open('json/ccacn.json', 'r') as file:
                json_data = json.load(file)

            channel.basic_publish(exchange='',
                                    routing_key='send_queue',
                                    body=json.dumps(json_data))
            print(" [x] Fichier JSON envoyé")
            quit()
        else:
            print("Code incorrect")
            quit() 

    channel.basic_consume(queue='auth_reponse', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    microservice_send()