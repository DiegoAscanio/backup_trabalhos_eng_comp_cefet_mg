/* ----- Utilizando o Arduino como uma fonte de tensao DC ----- */


const int Fonte_DC = 3; // O sinal de tensao "analogica" sera  
                        // transmitido pelo pino de saida digital 3 (PWM)

void setup(){

  pinMode(Fonte_DC, OUTPUT); // Define o pino 3 (Fonte_DC) como uma saida

}


void loop(){

  analogWrite(Fonte_DC, 255); // Escreve no pino 3 (Fonte_DC), que simulara
                             // uma saida analogica via PWM
                             // 0 corresponde a 0 V
                             // 255 corresponde a 5 V 

}



