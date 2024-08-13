#include "HWCDC.h"
#include "NimBLEDevice.h"
#include <Arduino.h>

#define LED_PIN 8

class MyFirstServerCallback : public NimBLEServerCallbacks {

  void onConnect(NimBLEServer *pServer) {
    Serial.println("Client Connected");

    pServer->startAdvertising();
  }

  void onDisconnect(NimBLEServer *pServer) {
    Serial.println("Client Disconnected");

    pServer->startAdvertising();
  }
};

class MyFirstCharacteristicCallback : public NimBLECharacteristicCallbacks {

  void onWrite(NimBLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();

    Serial.print("Received Value: ");
    Serial.println(value.c_str());

    if (value == "ON") {
      digitalWrite(LED_PIN, LOW);
      pCharacteristic->setValue("ON");
    } else if (value == "OFF") {
      digitalWrite(LED_PIN, HIGH);
      pCharacteristic->setValue("OFF");
    } else {
      Serial.println("Unknown Value Received");
    }
  }

  void onRead(NimBLECharacteristic *pCharacteristic) {
    Serial.println("Client Read Characteristic");
  }
};

void setup(void) {

  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  NimBLEDevice::init("HelloNimBLE");

  NimBLEServer *pServer = NimBLEDevice::createServer();
  pServer->setCallbacks(new MyFirstServerCallback);

  NimBLEService *pService =
      pServer->createService("93c07c1f-922c-437d-9d80-0449e6c4ae53");
  NimBLECharacteristic *pCharacteristic = pService->createCharacteristic(
      "f5580f27-af8f-4796-b4ed-47600d173ce9",
      NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::WRITE);
  pCharacteristic->setCallbacks(new MyFirstCharacteristicCallback());

  pService->start();
  pCharacteristic->setValue("Hello BLE");

  NimBLEAdvertising *pAdvertising = NimBLEDevice::getAdvertising();
  pAdvertising->addServiceUUID("6de1445f-9e7c-494f-944b-1a2259c0fc3b");
  pAdvertising->start();
}

void loop() {}
