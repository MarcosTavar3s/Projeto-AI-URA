# Importação das bibliotecas
import paho.mqtt.client as mqtt

# Cria o cliente do MQTT
client = mqtt.Client()

anterior = 0
atual = 1

# Conexão do MQTT
def on_connect(client, userdata, flags, rc):
    # Conectando ao broker 
    print(f"Conectado ao broker com código de resultado {rc}")
    
    global disconnectMqtt
    disconnectMqtt = False

    # Publicando no tópico 
    client.publish('aiurarecebe/anterior', 'MQTT conectado')
    client.publish('aiurarecebe/atual', 'MQTT')
    
    client.subscribe("aiurarecebe/atual")

# Impressão da mensagem recebida pelo tópico 
def on_message(client, userdata, msg):
    print(f'Mensagem de ${msg.topic}: ${msg.payload.decode()}')
    
    global anterior, atual 
    print(f'Anterior:{anterior} e Atual:{atual}')
    
    # if msg.topic =="aiurarecebe/atual":
    #     atual = msg.payload.decode()
    # elif 
    atual = msg.payload.decode()
        
    if anterior != atual:
        client.publish('aiurarecebe/anterior', 'mudanca:'+str(atual))
        print('é diferente')
        anterior = atual
    else:
        client.publish('aiurarecebe/anterior', 'permanece:'+str(atual))
        print('é igual')
    
    
    
    print(f'Anterior:{anterior} e Atual:{atual}')
  

# Desconectar do broker
def disconnect():
    global client
    print('Encerrando conexão com o broker...')
    client.disconnect()
    print('Conexão com o broker encerrada')

# Publicar mensagem no broker
def publish(msg):
    global client
    client.publish('aiurarecebe', msg)

# Função principal do MQTT
def main():    
    global mqttMessage
    global client

    client.on_connect = on_connect
    client.on_message = on_message

    broker = 'broker.emqx.io'
    client.connect(broker, 1883, 60)
    
    client.loop_forever()       


if _name_ == '_main_':
    main()
