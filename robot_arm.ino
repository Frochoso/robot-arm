#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_PWMServoDriver.h>

// --- SCREEN CONFIG ---
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// --- WIFI CONFIG ---
const char* ssid = "your network here";
const char* password = "network password here";
unsigned int localPort = 4210;
WiFiUDP udp;

// --- PCA9685 CONFIG ---
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN 150
#define SERVOMAX 600

// --- OTHER VARIABLES ---
unsigned long lastScreenTime = 0;
int angF = 90;
int angH = 90;

void setup() {
  Serial.begin(115200);

  // I2C init and screen
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 non detected"));
    for (;;)
      ;
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Initializing WiFi...");
  display.display();

  // Connect to WiFi network
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    display.print(".");
    display.display();
  }

  //SHOW IP
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("CONNECTED!");
  display.println("");
  display.print("IP: ");
  display.println(WiFi.localIP());
  display.display();

  //PCA9685
  pwm.begin();
  pwm.setPWMFreq(50);
  udp.begin(localPort);

  delay(2000);
}

void loop() {
  int packetSize = udp.parsePacket();

  if (packetSize) {
    char packetBuffer[255];
    int len = udp.read(packetBuffer, 255);
    if (len > 0) packetBuffer[len] = 0;

    String data = String(packetBuffer);
    int indexF = data.indexOf('F');
    int indexH = data.indexOf('H');

    if (indexF != -1 && indexH != -1) {
      int angF = data.substring(indexF + 1, indexH).toInt();
      int angH = data.substring(indexH + 1).toInt();

      // MOVE SERVOS
      pwm.setPWM(0, 0, map(constrain(angF, 0, 180), 0, 180, SERVOMIN, SERVOMAX));
      pwm.setPWM(1, 0, map(constrain(angH, 0, 180), 0, 180, SERVOMIN, SERVOMAX));
    }
  }


  unsigned long actualTime = millis();

  if (actualTime - lastScreenTime
      >= 200) {
    lastScreenTime = actualTime;

    display.clearDisplay();
    display.setCursor(0, 0);
    display.printf("IP: %s\n", WiFi.localIP().toString().c_str());
    display.println("---------------------");
    display.setTextSize(2);
    display.printf("ANT: %d\n", angF);
    display.printf("MAN: %d", angH);
    display.display();
  }
}