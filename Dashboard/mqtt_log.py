import paho.mqtt.client as mqtt
import time
from typing import Optional, Any

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

caminho_log = "log.txt"
log = None

def on_connect(client: mqtt.Client, userdata: Optional[Any], flags: dict[str, Any], rc: int) -> None:
    """
    Função de retorno ao conectar ao broker MQTT.
    
    Args:
        client: Objeto nativo do paho.mqtt.client
        userdata: Objeto arbitrário que pode ser associado ao cliente ao criar o cliente MQTT  (padrão é None).
        flags: Dicionário com informações adicionais sobre a conexão.
        rc: Código de retorno que indica o resultado da tentativa de conexão.
    
    Retorna:
        None.
    """
     
    print(f"Conectado ao broker com código de resultado {rc}")
    
    # Publicando no tópico 
    client.publish('aiurarecebe/atual', 'MQTT')    
    client.subscribe("aiurarecebe/atual")


def on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
    """
    Função para ler as mensagens MQTT e gravar em um arquivo.txt.
    
    Args:
        client: Objeto nativo do paho.mqtt.client.
        userdata: Objeto arbitrário que pode ser associado ao cliente ao criar o cliente MQTT  (padrão é None).
        msg: Um objeto do tipo MQTTMessage que contém informações sobre a mensagem recebida, como o tópico e o payload.
        
    Retorna:
        None.
    """
    
    print(f'Mensagem de ${msg.topic}: ${msg.payload.decode()}')
     
    atual = msg.payload.decode()    
    
    with open(caminho_log,'a') as arquivo:
        nova_mensagem = f'{time.strftime("%d/%m/%y %H:%M:%S")}: {atual}'
        arquivo.write(nova_mensagem+'\n')


def disconnect() -> None:
    """
    Função para desconectar do broker MQTT.
    
    Args:
        None.
            
    Retorna:
        None.
    """
    
    global client
    
    print('Encerrando conexão com o broker...')
    client.disconnect()
    print('Conexão com o broker encerrada')


def main() -> None: 
    """
    Função principal que chama a conexão do broker e mantém a conexão viva indefinidamente.
    
    Args:
        None.
    
    Retorna:
        None.
    """
           
    global mqttMessage
    global client

    client.on_connect = on_connect
    client.on_message = on_message

    broker = 'broker.emqx.io'
    client.connect(broker, 1883, 60)
    
    client.loop_forever()       


if __name__ == '__main__':
    main()
