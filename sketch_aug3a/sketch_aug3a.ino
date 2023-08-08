#include <FastLED.h>

#define LED_PIN 3
#define NUM_LEDS 144

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  if (Serial.available() >= 9) { // 9 bytes for 3 RGB values and brightness (e.g., "255255255100")
    char rgbData[9];
    Serial.readBytes(rgbData, 9);

    int r = atoi(&rgbData[0]);
    int g = atoi(&rgbData[3]);
    int b = atoi(&rgbData[6]);
    int brightness = atoi(&rgbData[7]);

    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB(r, g, b);
      leds[i].fadeToBlackBy(255 - brightness);
    }
    FastLED.show(); // Smoothly fade the brightness of all LEDs at once
    
    // delay(20); // Add a delay of 20 milliseconds between LED updates
  }
}
