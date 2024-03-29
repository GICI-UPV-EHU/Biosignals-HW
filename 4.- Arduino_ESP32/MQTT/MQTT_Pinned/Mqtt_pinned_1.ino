#include <Arduino.h>
#include <MAX30105.h>
#include <ESP32Time.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>


MAX30105 particleSensor;
// Constantes necesarias para la conexión WIFI
const char* ssid = "A019";  // Nombre de la red
const char* password = "bfxDsZZAF33SAA";  // Contraseña de la red
// const char* ssid = "GICI";
// const char* password = "delfingiciehu";

// La IP de dónde se encuentra el broker MQTT (Raspberry) --No es estática
const char* mqtt_server = "192.168.1.138"; 
// const char* mqtt_server = "192.168.0.104";

// Crando el cliente para el mqtt
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];

// Variables para NTP -- hora actual
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 3600; // Offset pata UTC+1

// Configuración del reloj interno de la ESP32
ESP32Time rtc(3600);  // offset no necesario ya que se introduce en NTP
#define configTICK_RATE_HZ ((TickType_t)1000); // Se define que haya 1 interrupción cada milisegundo


// Se introducen las variables para la Tarea GSR
const TickType_t freq_GSR = 1000; // Se establece una frecuencia de muestreo de 1Hz
const int puerto_GSR =36; // El número del puerto al que va conectado el cable GSR


// Se designan los nombres para la TareaPOX
const TickType_t freq_POX = 100; // Se establace una frecuencia de muestreo de 10Hz

// Se designan los nombres para la TareaPOX
const TickType_t freq_ECG = 10; // Se establace una frecuencia de muestreo de 100Hz
const int puerto_ECG = 39; // El número del puerto al que va conectado la señal ECG

//----------------------------------------------------------------------------//

// Función para la conexión al WIFI 
void setup_wifi() 
{

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
// Función para la conexión con el Broker MQTT de la RasPi
void conexionMQTT()
{
  client.setServer(mqtt_server, 1883);
  delay(1000); // Se espera 1 segundo para dar tiempo a que haga la conexión
  int a = 1;  // Variable para entrar al bucle while
  while (a!=0)
  {
    if (client.connect("esp32")) 
    {
      // connection succeeded
      Serial.println("Connected ");
      boolean r = client.subscribe("esp32_ima/inci");
      a = client.state();
    } 
    else 
    {
      // connection failed
      a = client.state(); //te devuelve un int ---> El tipo de error: https://pubsubclient.knolleary.net/api#state
      Serial.println("Connection failed ");
      Serial.println(a);
      delay(5000); 
    }
  }
}
// Función para la configuración de la hora 
void configHora()
{
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  struct tm timeinfo;
  if (getLocalTime(&timeinfo))
  {
    rtc.setTimeStruct(timeinfo); 
  }  
  
  Serial.print("Fecha Actual: ");
  printLocalTime();
  String Time = printLocalTime();
  Serial.println(Time);
}
// Función para escrbir la hora en forma de string
String printLocalTime()
{
  String horas, fecha;
  int mes, dia, ano;
  //horas= rtc.getTime("%d/%B/%Y %H:%M:%S."); // hay q pasar el mes a numero para que se entineda como timstamp
  horas = rtc.getTime();
  mes = rtc.getMonth() + 1;
  dia = rtc.getDay();
  ano = rtc.getYear();     
  String millis;
  millis = rtc.getMillis();
  if (millis.length()==1)
  {
    millis = "00" + millis;
  }
  else if (millis.length()==2)
  {
    millis = "0" + millis;
  }   
  fecha = String(ano) + "-" + String(mes) + "-" + String(dia) + " " + horas + "." + millis;
  return fecha;
}
// Función para la configuración del sensor MAX30102 (Pulsioxímetro)
void configMax30102()
{
  // Configuración del sensor MAX30102
  while(particleSensor.begin(Wire, I2C_SPEED_FAST) == false) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    delay(5000);
  }
  // I have changed the ledbrightness
  byte ledBrightness = 35; //Options: 0=Off to 255=50mA - 255
  byte sampleAverage = 4; //Options: 1, 2, 4, 8, 16, 32
  // I have changed the ledmode
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  int sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200 - 400
  int pulseWidth = 411; //Options: 69, 118, 215, 411 -69
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384 - 16834
 
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);

  
}
void setup() 
{
  Serial.begin(115200); // Se inicia la comunicación por medio del puerto USB 
  setup_wifi();  // Se conecta al wifi indicado
  conexionMQTT(); // Se conecta al Broker MQTT
  configHora();
  configMax30102();
  
 // Una vez esta hecha la conexión, se pasa a lanzar las Tareas Periodicas
  xTaskCreatePinnedToCore(TareaGSR_code, "Task GSR", 4960, NULL, 10, NULL,0);   

  xTaskCreatePinnedToCore(TareaPOX_code, "Task POX", 4960, NULL, 20, NULL,1); 
  
  xTaskCreatePinnedToCore(TareaECG_code, "Task ECG", 4960, NULL, 30, NULL,0);   
}

// Código para la ejecución ciclica de la Tarea de la señal GSR
void TareaGSR_code (void* paremeter)
{
  // Valores necesarios parala creación del mensaje a enviar por mqtt 
  // Mensaje: Tiempo;ValorResistencia
  String Time;
  String Mensaje;
  String Res_act;
  char buffer[50];
  TickType_t t_ult;

  // Para intentar mejorar la respuesta del sistema, se trata de separar la
  // tara GSR 8ms de la otra tarea que se ejecuta en el mismo procesador POX
  
  t_ult = xTaskGetTickCount();  // Se toma el tiempo actual
  const TickType_t t_s = 5;     // Se introduce el tiempo que se quiere esperar
  vTaskDelayUntil(&t_ult, t_s); // Se le manda a la tarea esperar, hasta que sea el t_utl + 8 ms

  Serial.println("Comienza la Tarea GSR");
  t_ult = xTaskGetTickCount(); // Se toma los ticks en el instante inicial

  while(1)
  {
    vTaskDelayUntil(&t_ult, freq_GSR);
    
    while(!client.connect("esp32")) 
    {
    client.setServer(mqtt_server, 1883); 
    Serial.print("Perdí conexión");     
    }
    
    Time = printLocalTime();
    int vLeido = analogRead(puerto_GSR);
    // Cálculo de la resistencia
    float valorReal = vLeido * (3.3/4096)/21;

    float vResis = (5.0/valorReal-1)*4700;

    float vSiem = (1/vResis)*1000000;
    Res_act = String(vSiem,4);
    
    //Serial.println(Mensaje); 
    Mensaje = Time + "," + Res_act;  
    Mensaje.toCharArray(buffer,50);

    //Serial.println(buffer);
    client.publish("esp32_ima/GSR",buffer); 
  }
 
}
// Código para la ejecución ciclica de la Tarea de la señal POX
void TareaPOX_code (void* paremeter)
{
  // Valores necesarios parala creación del mensaje a enviar por mqtt 
  // Mensaje: Tiempo;Rojo;infra
  String Time;
  String Mensaje;
  String Ro_a,Ir_a;
  char buffer[200];
  int rojo,infra;
  int pas = 0;
  TickType_t t_ult;
  
  Serial.println("Comienza la Tarea POX");

  t_ult = xTaskGetTickCount(); // Se toma los ticks en el instante inicial

  while(1)
  {
    vTaskDelayUntil(&t_ult, freq_POX);
    
    Time = printLocalTime();
    rojo =particleSensor.getRed();
    infra = particleSensor.getIR();
    Ro_a = String(rojo);
    Ir_a = String(infra);   
    ///////////////////////////////////////
    pas = pas + 1;
    if (pas == 1)
    {
      Mensaje = Time + "," + Ro_a + "," + Ir_a;    
    }
    else if (pas == 3)
    {
      Mensaje = Mensaje + "," + Time + "," + Ro_a + "," + Ir_a;
      Mensaje.toCharArray(buffer,200);
      client.publish("esp32_ima/POX",buffer); 
      pas = 0;
      Mensaje="";
    }
    else 
    {
      Mensaje = Mensaje + "," + Time + "," + Ro_a + "," + Ir_a;      
    }

  }
 
}
// Código para la ejecución ciclica de la Tarea de la señal ECG
void TareaECG_code (void* paremeter)
{
  // Valores necesarios parala creación del mensaje a enviar por mqtt 
  // Mensaje: Tiempo;Rojo;infra
  String Time;
  String Mensaje;

  int ECG_val;
  String Ecg_a;

  char buffer[200];
  int pas = 0;
  TickType_t t_ult;

  Serial.println("Comienza la Tarea ECG");

  t_ult = xTaskGetTickCount(); // Se toma los ticks en el instante inicial

  while(1)
  {
    vTaskDelayUntil(&t_ult, freq_ECG);

    Time = printLocalTime();
    ECG_val = analogRead(puerto_ECG);
    Ecg_a = String(ECG_val);
  
    ///////////////////////////////////////
    pas = pas + 1;
    if (pas == 1)
    {
      Mensaje = Time + "," + Ecg_a;
    }
    else if (pas == 5)
    {
      Mensaje = Mensaje + "," + Time + "," + Ecg_a;
      Mensaje.toCharArray(buffer,500);
      client.publish("esp32_ima/ECG",buffer); 
      pas = 0;
      Mensaje="";
      //Serial.println(buffer);
    }
    else 
    {
      Mensaje = Mensaje + "," + Time + "," + Ecg_a;   
    }

  }
 
}

// La parte ciclica no es encesaria ya que las tareas se hará mediante
// interrupciones de forma periódica
void loop() 
{
}
