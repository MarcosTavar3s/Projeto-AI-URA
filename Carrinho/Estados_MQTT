#include <stdio.h>
#include <string.h>
#include <mqtt_client.h>


const char* proximo_topic = "aiurarecebe/proximo";
const char* atual_topic = "aiurarecebe/atual";


char atual_msg[256] = "";
char proximo_msg[256] = "";


void atualiza_estados(const char* topic, const char* msg) {
    if (strcmp(topic, proximo_topic) == 0) {
        strncpy(proximo_msg, msg, sizeof(proximo_msg) - 1);
        proximo_msg[sizeof(proximo_msg) - 1] = '\0';
    } else if (strcmp(topic, atual_topic) == 0) {
        strncpy(atual_msg, msg, sizeof(atual_msg) - 1);
        atual_msg[sizeof(atual_msg) - 1] = '\0';
    }


    // Verifica se as mensagens são diferentes ou se o estado continua o mesmo
    if (strcmp(atual_msg, proximo_msg) != 0 && strlen(proximo_msg) > 0) {
        // Se forem diferentes, a mensagem enviada vira o estado atual 
        mqtt_publish(atual_topic, proximo_msg);
        strncpy(atual_msg, proximo_msg, sizeof(atual_msg) - 1); // Atualizar atual_msg
    }
}

