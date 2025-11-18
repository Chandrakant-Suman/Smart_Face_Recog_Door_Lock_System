// esp32cam_post_motion.ino
#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// PIR and buzzer pins 
#define PIR_PIN 13
#define BUZZER_PIN 14


// camera pin connection
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

const char* ssid = ":):";
const char* password = "km3ggnznvew9";
const char* serverUrl = "http://10.246.215.164:5000/recognize";  //server and esp should be on same network

void startCameraServer(){} 

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  // Camera init
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  // init with high specs to improve recognition
  if(psramFound()){
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    while(true);
  }

  // WiFi connection
  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected. IP: ");
  Serial.println(WiFi.localIP());
}

unsigned long lastTrigger = 0;
const unsigned long debounceMs = 2000; // ignore new triggers for 2s

void loop() {
  int pir = digitalRead(PIR_PIN);
  if (pir == HIGH && (millis() - lastTrigger) > debounceMs) {
    lastTrigger = millis();
    Serial.println("[EVENT] Motion detected!");
    // take photo
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed");
      return;
    }
    // POST image
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverUrl);
      http.addHeader("Content-Type", "image/jpeg");
      int httpCode = http.POST(fb->buf, fb->len);
      if (httpCode > 0) {
        String payload = http.getString();
        Serial.printf("Server response: %d %s\n", httpCode, payload.c_str());
        
        if (payload.indexOf("\"known\"") != -1) {
          Serial.println("door unlocked"); 
          // optionally trigger a relay here to unlock
        } else if (payload.indexOf("\"unknown\"") != -1) {
          Serial.println("unknown person - buzzer!");
          // ring buzzer for 3s
          digitalWrite(BUZZER_PIN, HIGH);
          delay(3000);
          digitalWrite(BUZZER_PIN, LOW);
        } else if (payload.indexOf("\"no_face\"") != -1) {
          Serial.println("no face detected");
        } else {
          Serial.println("unrecognized response");
        }
      } else {
        Serial.printf("POST failed, error: %s\n", http.errorToString(httpCode).c_str());
      }
      http.end();
    } else {
      Serial.println("WiFi disconnected");
    }
    esp_camera_fb_return(fb);
  }
  delay(200);
}



