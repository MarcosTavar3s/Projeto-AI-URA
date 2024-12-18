# Importação das bibliotecas
import paho.mqtt.client as mqtt

# Cria o cliente do MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

historico = 0
atual = 1

# Conexão do MQTT
def on_connect(client, userdata, flags, rc):
    # Conectando ao broker 
    print(f"Conectado ao broker com código de resultado {rc}")
    
    global disconnectMqtt
    disconnectMqtt = False

    # Publicando no tópico 
    client.publish('aiurarecebe/historico', 'MQTT conectado')
    client.publish('aiurarecebe/atual', 'MQTT')
    
    client.subscribe("aiurarecebe/atual")

# Impressão da mensagem recebida pelo tópico 
def on_message(client, userdata, msg):
    print(f'Mensagem de ${msg.topic}: ${msg.payload.decode()}')
    
    global historico, atual 
    print(f'Anterior:{historico} e Atual:{atual}')
    
    atual = msg.payload.decode()
        
    if historico != atual:
        client.publish('aiurarecebe/historico', 'Mudanca:'+str(atual))
        print('é diferente')
        historico = atual
    else:
        client.publish('aiurarecebe/historico', 'Permanece:'+str(atual))
        print('é igual')
    
    
    
    print(f'Anterior:{historico} e Atual:{atual}')
  

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


if __name__ == '__main__':
    main()
