#include <Arduino.h>
#include <MAX30105.h>
#include <ESP32Time.h>
#include <WiFiClientSecure.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
// Se le da nombre a la clase del sensor 
MAX30105 particleSensor;
// Constantes necesarias para la conexión WIFI
      // const char* ssid = "Imanol Wifi";  // Nombre de la red
      // const char* password = "123456789";  // Contraseña de la red
const char* ssid = "GICI";
const char* password = "delfingiciehu";

// La IP de dónde se encuentra el broker MQTT (Raspberry) --No es estática
        //const char* mqtt_server = "192.168.1.137"; 
const char* mqtt_server = "192.168.0.100";

// El certificado CA para conectarse correctamente al MQTT (SSL)
const char* ca_cert  =
"-----BEGIN CERTIFICATE-----\n" \
"MIIDNzCCAh+gAwIBAgIUH3nb+KkVnad7Lq/WEnEvaOpQa5IwDQYJKoZIhvcNAQEL\n" \
"BQAwKjEQMA4GA1UECgwHVVBWX0VIVTEWMBQGA1UEAwwNMTkyLjE2OC4wLjEwMDAg\n" \
"Fw0yMzAxMjYyMjM1MDNaGA8yMTIzMDEwMjIyMzUwM1owKjEQMA4GA1UECgwHVVBW\n" \
"X0VIVTEWMBQGA1UEAwwNMTkyLjE2OC4wLjEwMDCCASIwDQYJKoZIhvcNAQEBBQAD\n" \
"ggEPADCCAQoCggEBAMETjUTul20o8Jhe+GvidLchZf47PJO0fOdOeMdoDO0l9epo\n" \
"YZiHgZ9idH5ai3LWZ/iVL8GzHgiouYl0A1gRfsdyFjjYO8KK9FQ70WCE7ldGLJvb\n" \
"MQxaq7o/9iIMkQCmPY8GMCFfjJm++PlZhY7KON3fRz9ZDKB/TqXiv8q0jro7X9/L\n" \
"QhsQXow7q83h7vN0RULr11N5P8pgNrXBRnpnXpyyugP7tBVlJlRulHul380eeI4Y\n" \
"OJ7VGHcrQ+ieUs55C7Ay6GAapaqj7qWUq1zRazGwXVhcPtFnMOgn9lMWaeccXDat\n" \
"PdrLswl0/RjJxVnDmq2OZW7+s5Jxbu74y4wfmaUCAwEAAaNTMFEwHQYDVR0OBBYE\n" \
"FI2dcEViig4cxWvurtyP3Ux4vcNSMB8GA1UdIwQYMBaAFI2dcEViig4cxWvurtyP\n" \
"3Ux4vcNSMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAAVc0Pq4\n" \
"0mFKfATVhquo1ldR/eKwZj487r2yDgGViiKagB4iccJHVeahUYbOJ1VoWrkhIh6i\n" \
"Vp7co4FfmVdFYa40A3gNP2TaiKIsMZ8ljKW/7QnEflnK/RODrgKpsVyHTGVChqIj\n" \
"ts8mKDB+38qG8ZO6Q/bPfuD8lFZUxCm+TcELW+pfdcYrGetKf4kumUQsI1N7Vv3n\n" \
"Q3xzwQ0niwRGc669lTpV2QPgphvTZsw6whnYsfDcHsv6DtHSU4BgGmY1FUcOL/92\n" \
"Ux9UPKzM8zONqMOKSVXwExj7rtb+bUbGldJdtUjMM3tlArYeoUDtxgduBu2d7xQ2\n" \
"ooPTKJUPgrSiIMM=\n" \
"-----END CERTIFICATE-----\n";

// Crando el cliente para el mqtt
WiFiClientSecure espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

// Se crean y asignan valores a las variables necesarias para las tareas
#define configTICK_RATE_HZ ((TickType_t)1000);
// Se designan los nombres de la TareaGSR
TaskHandle_t Tarea_GSR;

const int puerto_GSR =36; // El número del puerto al que va conectado el cable GSR
const int puerto_ECG =4; // El número del puerto al que va conectado la señal ECG (ya tratada)

// Se designan los nombres para la TareaPOX
TaskHandle_t TareaPOX;

// NTP -- hora actual
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 3600;

ESP32Time rtc(3600);  // offset en ssegundos --> GMT+1


//----------------------------------------------------------------------------//

// Función para la conexión al WIFI -- Código de ejemplo
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
void conexionMQTT()
{
  espClient.setCACert(ca_cert);
  client.setServer(mqtt_server, 8883);
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

void configMax30102()
{
  // Configuración del sensor MAX30102
  while(particleSensor.begin(Wire, I2C_SPEED_FAST) == false) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    delay(5000);
  }
  // I have changed the ledbrightness
  byte ledBrightness = 255; //Options: 0=Off to 255=50mA - 255
  byte sampleAverage = 1; //Options: 1, 2, 4, 8, 16, 32
  // I have changed the ledmode
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  int sampleRate = 1000; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200 - 400
  int pulseWidth = 69; //Options: 69, 118, 215, 411 -69
  int adcRange = 16384; //Options: 2048, 4096, 8192, 16384 - 16834
 
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);

  
}
void setup() 
{
  Serial.begin(115200); // Se inicia la comunicación por medio del puerto USB 
  pinMode(26, INPUT); // Setup for leads off detection LO +
  pinMode(27, INPUT); // Setup for leads off detection LO -
 
  setup_wifi();  // Se conecta al wifi indicado
  conexionMQTT(); // Se conecta al Broker MQTT
  configHora();
  configMax30102();
  
 // Una vez esta hecha la conexión, se pasa a lanzar las Tareas Periodicas
  // xTaskCreatePinnedToCore(TareaGSR_code, "Task GSR", 4960, NULL, 10, NULL,0);   

 //  xTaskCreatePinnedToCore(TareaPOX_code, "Task POX", 4960, NULL, 20, NULL,1); 
  
  xTaskCreatePinnedToCore(TareaECG_code, "Task ECG", 4960, NULL, 30, NULL,0);   
}


void TareaGSR_code (void* paremeter)
{
  // Valores necesarios parala creación del mensaje a enviar por mqtt 
  // Mensaje: Tiempo;ValorResistencia
  String Time;
  String Mensaje;
  String Res_act;
  char buffer[50];
  TickType_t t_ult;
  const TickType_t freq = 1000; // Se establece un periodo de 1s = 1000ms

  // Para intentar mejorar la respuesta del sistema, se trata de separar la
  // tara GSR 8ms de la otra tarea que se ejecuta en el mismo procesador POX
  
  t_ult = xTaskGetTickCount();  // Se toma el tiempo actual
  const TickType_t t_s = 5;     // Se introduce el tiempo que se quiere esperar
  vTaskDelayUntil(&t_ult, t_s); // Se le manda a la tarea esperar, hasta que sea el t_utl + 8 ms

  Serial.println("Comienza la Tarea 1");
  t_ult = xTaskGetTickCount(); // Se toma los ticks en el instante inicial

  while(1)
  {
    vTaskDelayUntil(&t_ult, freq);
    
    while(!client.connect("esp32")) 
    {
      espClient.setCACert(ca_cert);
      client.setServer(mqtt_server, 8883); 
      Serial.print("Perdí conexión");     
    }
    
    Time = printLocalTime();
    int vLeido = analogRead(puerto_GSR);
    // Cálculo de la resistencia
    float valorReal = vLeido * (3.3/4096)/21;

    float vResis = (5/valorReal-1)*4700;

    float vSiem = (1/vResis)*1000000;
    Res_act = String(vSiem,4);
    
    //Serial.println(Res_act); 
    Mensaje = Time + "," + Res_act;    
    Mensaje.toCharArray(buffer,50);
    //Serial.print(buffer);

    //Serial.println(buffer);
    client.publish("esp32_ima/GSR",buffer); 
  }
 
}

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
  const TickType_t freq = 100; // Se establace que haya 1 muestra cada 10 ticks --> 100 muestras/s
  Serial.println("Comienza la Tarea 2");

  t_ult = xTaskGetTickCount(); // Se toma los ticks en el instante inicial

  while(1)
  {
    vTaskDelayUntil(&t_ult, freq);
    
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
    else if (pas == 5)
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
  const TickType_t freq = 10; // Se establace que haya 1 muestra cada 10 ticks --> 100 muestras/s

  Serial.println("Comienza la Tarea ECG");

  t_ult = xTaskGetTickCount(); // Se toma los ticks en el instante inicial

  while(1)
  {
    vTaskDelayUntil(&t_ult, freq);
    if((digitalRead(26) == 1)||(digitalRead(27) == 1))
    {
      ECG_val = 0;
    }
    else
    {
    // send the value of analog input 0:
      ECG_val = (analogRead(4));
    }
    Time = printLocalTime();
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


void loop() 
{
}