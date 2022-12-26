#include <WiFiClientSecure.h>
#include <esp_crt_bundle.h>
#include <ssl_client.h>

#include <WiFi.h>

#include <PubSubClient.h>

const char* ssid = "GICI";
const char* password = "delfingiciehu";

const char* mqtt_server = "192.168.0.104";

const char* ca_cert  = 
"-----BEGIN CERTIFICATE-----\n"\
"MIIDlzCCAn+gAwIBAgIUf5waOXhwawLKeNXuqSXxVyIwCbEwDQYJKoZIhvcNAQEL\n"\
"BQAwWjELMAkGA1UEBhMCRVMxEDAOBgNVBAgMB0JpemthaWExDzANBgNVBAcMBkJp\n"\
"bGJhbzEQMA4GA1UECgwHVVBWL0VIVTEWMBQGA1UEAwwNMTkyLjE2OC4wLjEwNDAg\n"\
"Fw0yMjEwMjUxMzA2NDJaGA8yMTIyMTAwMTEzMDY0MlowWjELMAkGA1UEBhMCRVMx\n"\
"EDAOBgNVBAgMB0JpemthaWExDzANBgNVBAcMBkJpbGJhbzEQMA4GA1UECgwHVVBW\n"\
"L0VIVTEWMBQGA1UEAwwNMTkyLjE2OC4wLjEwNDCCASIwDQYJKoZIhvcNAQEBBQAD\n"\
"ggEPADCCAQoCggEBAMIwNjl0MtIK0MTGOjUXZQe/MJ1Pz4fLLXGA6dYSdFGKzc+b\n"\
"4ay1D4dR8sE3pyAjwwgKYROB3P/+L8KlqA+WUTOMZM6qXbeWr2vlHl2tWtVZOhwd\n"\
"dWxcAT2TNafS6JzSr2ZbslYBeJHgx28frcfYIPADc7yz1lqovJbYbqcXmi5GtnMy\n"\
"4yD7HkO2gq9zK0yPTTDO8kqp1H+T+LPw99UaXP+/XBOg8QmjERfIkY0ZP8k+J7PD\n"\
"URpE/EvkFdX1HRUVt/Kq9At7f7C2uLOJlrOwieLj/aimjdxI1BgvSKmXsE0romI5\n"\
"BLcUrDtyS48t4pU1NgYkcXKkwAIB4c0u2eAz/EUCAwEAAaNTMFEwHQYDVR0OBBYE\n"\
"FI3WmHbBt+AuzD4c6+krLRUxO/cOMB8GA1UdIwQYMBaAFI3WmHbBt+AuzD4c6+kr\n"\
"LRUxO/cOMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAAq5ych+\n"\
"E1I2caNENeL3vAc+1NCg4GzEZR45kHyIu49ApTkgdk9ynTNBDpdSEQQ9cECODXo+\n"\
"Hv1ajLlG340UWSvhkOepTZrAwyPGEpgmdKYN4HZ0c+La0VedoGqWR473xWIivz+9\n"\
"zA7rs0IwV2zI8k9gy4vGPaMoO65F71/3vY7gFzfv1+TQS7dtnoCloMd8t2sc9/bn\n"\
"ojE0nE6PqrZ/nHj0tty5W265Shl9P6QkBX/+Q0yaUsuki0OD3v0os/7WQjP5dpAo\n"\
"tLjNaOgeVKn4RcqHQAeTURnYO5HHaocpddflXevc73VttgwShOVeIrBTnljvHruE\n"\
"MVS7AYyB05pcCoY=\n"\
"-----END CERTIFICATE-----\n";

WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup()
{
  Serial.begin(115200);
  Serial.println();
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");

  }
  Serial.println();  
  Serial.print("WiFi Connected: -IP: ");
  Serial.println(WiFi.localIP());

  espClient.setCACert(ca_cert);
  client.setServer(mqtt_server, 8883);

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


void loop(){

}