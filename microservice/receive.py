import pika, json
from pymongo import MongoClient

def jsonreceive():
# Connexion à la base de données MongoDB
  client = MongoClient('mongodb', 27017)
  db = client['OFPPT']
  collection = db['DEVOWFS201']
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
  channel = connection.channel()

  channel.queue_declare(queue='send_queue')

  def callback(ch, method, properties, body):
    json_data = json.loads(body.decode('utf-8'))
    print(" [x] Réception du fichier JSON : %r" % json_data)
    # Insérer les données dans la base de données MongoDB
    result = collection.insert_one(json_data)
    print(" [x] Données insérées avec succès dans MongoDB :", result.inserted_id)

  channel.basic_consume(queue='send_queue', on_message_callback=callback, auto_ack=True)
  print('En attente de messages. Pour quitter, appuyez sur CTRL+C')  
  channel.start_consuming()

if __name__ == '__main__':  
   jsonreceive()  
