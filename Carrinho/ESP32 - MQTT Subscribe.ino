#include <WiFi.h>
#include <PubSubClient.h>

#define M1 32
#define M2 33
#define S1 26
#define S2 27

// Configurações da rede Wi-Fi
const char* ssid = "XXXXXX";
const char* password = "XXXXXX";

// Configurações do broker MQTT
const char* mqtt_server = "broker.emqx.io";
const char* topic = "XXXXXX";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(M1,OUTPUT);
  pinMode(M2,OUTPUT);
  pinMode(S1,OUTPUT);
  pinMode(S2,OUTPUT);
}

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado ao Wi-Fi");
}

void movimento(int velocidadem1, int velocidadem2, int velocidades1, int velocidades2){
  analogWrite(M1,velocidadem1);
  analogWrite(M2,velocidadem2);
  analogWrite(S1,velocidades1);
  analogWrite(S2,velocidades2);
}
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Mensagem recebida do tópico: ");
  Serial.println(topic);
  Serial.print("Mensagem: ");
  String msg;
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    msg+=(char)message[i];
  }

  if(msg.equals("F")){
    movimento(0,255,0,255);
    Serial.println("Carro para frente");
  }
  if(msg.equals("T")){
    movimento(255,0,255,0);
    Serial.println("Carro para trás");    
  }
  if(msg.equals("D")){
    movimento(0,255,255,0);
    Serial.println("Carro para direita");    
  }
  if(msg.equals("E")){
    movimento(255,0,0,255);
    Serial.println("Carro para esquerda");    
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) {
      client.subscribe(topic);
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
