// webserver vars
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define WIFI_SSID "thinkAP"
#define WIFI_PASS "penguinPinapplePizza"
ESP8266WebServer server(80);

// led vars
#include "FastLED.h"
#define NUM_LEDS 60
CRGB leds[NUM_LEDS];
#define PIN 4

int r = 0, g = 0, b = 0;
bool effectsEnabled = false;
int currentEffect = 0; // look at effects in switch case statement below

// for strobe
int strobeCount = 10;
int flashDelay = 50;
int endPause = 1000;
// for running
int waveDelay = 50;
// for colorWipe
int speedDelay = 50;
// fire
int cooling = 55;
int sparking = 120;
int fireSpeedDelay = 15;

// led functions
void setPixel(int Pixel, byte red, byte green, byte blue) {
   leds[Pixel].r = red;
   leds[Pixel].g = green;
   leds[Pixel].b = blue;
}

void setAll(byte red, byte green, byte blue) {
  for(int i = 0; i < NUM_LEDS; i++ ) {
    setPixel(i, red, green, blue);
  }
  FastLED.show();
}

/*
 * EFFECTS
 */
void fade() {
  float red, green, blue;
     
  for(int k = 0; k < 256; k=k+1) {
    red = (k/256.0)*r;
    green = (k/256.0)*g;
    blue = (k/256.0)*b;
    setAll(red,green,blue);
    FastLED.show();
  }
     
  for(int k = 255; k >= 0; k=k-2) {
    r = (k/256.0)*red;
    g = (k/256.0)*green;
    b = (k/256.0)*blue;
    setAll(r,g,b);
    FastLED.show();
  }
}

void rgbFade() {
  for(int j = 0; j < 3; j++ ) {
    // Fade IN
    for(int k = 0; k < 256; k++) {
      switch(j) {
        case 0: setAll(k,0,0); break;
        case 1: setAll(0,k,0); break;
        case 2: setAll(0,0,k); break;
      }
      FastLED.show();
      delay(3);
    }
    // Fade OUT
    for(int k = 255; k >= 0; k--) {
      switch(j) {
        case 0: setAll(k,0,0); break;
        case 1: setAll(0,k,0); break;
        case 2: setAll(0,0,k); break;
      }
      FastLED.show();
      delay(3);
    }
  }
}
void strobe() {
  for(int j = 0; j < strobeCount; j++) {
    setAll(r, g, b);
    FastLED.show();
    delay(flashDelay);
    setAll(0,0,0);
    FastLED.show();
    delay(flashDelay);
  }
 
 delay(endPause);
}
void runnin() {
  int Position=0;
 
  for(int j=0; j<NUM_LEDS*2; j++)
  {
      Position++; // = 0; //Position + Rate;
      for(int i=0; i<NUM_LEDS; i++) {
        // sine wave, 3 offset waves make a rainbow!
        //float level = sin(i+Position) * 127 + 128;
        //setPixel(i,level,0,0);
        //float level = sin(i+Position) * 127 + 128;
        setPixel(i,((sin(i+Position) * 127 + 128)/255)*r,
                   ((sin(i+Position) * 127 + 128)/255)*g,
                   ((sin(i+Position) * 127 + 128)/255)*b);
      }
     
      FastLED.show();
      delay(waveDelay);
  }
}
void colorWipe() {
  for(uint16_t i=0; i<NUM_LEDS; i++) {
      setPixel(i, r, g, b);
      FastLED.show();
      delay(speedDelay);
  }
}
void rainbowCycle() {
  
}
void fire() {
  static byte heat[NUM_LEDS];
  int cooldown;
 
  // Step 1.  Cool down every cell a little
  for( int i = 0; i < NUM_LEDS; i++) {
    cooldown = random(0, ((cooling * 10) / NUM_LEDS) + 2);
   
    if(cooldown>heat[i]) {
      heat[i]=0;
    } else {
      heat[i]=heat[i]-cooldown;
    }
  }
 
  // Step 2.  Heat from each cell drifts 'up' and diffuses a little
  for( int k= NUM_LEDS - 1; k >= 2; k--) {
    heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3;
  }
   
  // Step 3.  Randomly ignite new 'sparks' near the bottom
  if( random(255) < sparking ) {
    int y = random(7);
    heat[y] = heat[y] + random(160,255);
    //heat[y] = random(160,255);
  }

  // Step 4.  Convert heat to LED colors
  for( int j = 0; j < NUM_LEDS; j++) {
    // Scale 'heat' down from 0-255 to 0-191
    byte t192 = round((heat[j]/255.0)*191);
   
    // calculate ramp up from
    byte heatramp = t192 & 0x3F; // 0..63
    heatramp <<= 2; // scale up to 0..252
   
    // figure out which third of the spectrum we're in:
    if( t192 > 0x80) {                     // hottest
      setPixel(j, 255, 255, heatramp);
    } else if( t192 > 0x40 ) {             // middle
      setPixel(j, 255, heatramp, 0);
    } else {                               // coolest
      setPixel(j, heatramp, 0, 0);
    }
  }

  FastLED.show();
  delay(fireSpeedDelay);
}
void meteorRain() {
  byte red = 0xff;
  byte green = 0xff;
  byte blue = 0xff;
  byte meteorSize = 10;
  byte meteorTrailDecay = 64;
  boolean meteorRandomDecay = true;
  int speedDelay = 30;
  
  setAll(0,0,0);
 
  for(int i = 0; i < NUM_LEDS+NUM_LEDS; i++) {
    // fade brightness all LEDs one step
    for(int j=0; j<NUM_LEDS; j++) {
      if( (!meteorRandomDecay) || (random(10)>5) ) {
        leds[j].fadeToBlackBy( meteorTrailDecay );       
      }
    }
   
    // draw meteor
    for(int j = 0; j < meteorSize; j++) {
      if( ( i-j <NUM_LEDS) && (i-j>=0) ) {
        setPixel(i-j, red, green, blue);
      }
    }
   
    FastLED.show();
    delay(speedDelay);
  }
}

/* 
 * Main Program code
 */
void setup() {
  Serial.begin(115200);
  Serial.println("Starting up....");

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);

  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("My IP: ");
  Serial.println(WiFi.localIP());  

  server.on("/", root);
  server.on("/rgb", rgb);
  server.on("/effect", effect);
  server.onNotFound(notFound);
  server.begin();
  Serial.println("HTTP server started");

  FastLED.addLeds<WS2811, PIN, GRB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  Serial.println("Leds initialized!");
}

void root() {
  server.send(200, "text/plain", "On root page");
}

void rgb() {
  String sendStr = "on rgb page";
  if(server.hasArg("hex") && server.hasArg("brightness")) {
    Serial.print(server.arg("hex"));
    Serial.print(" ");
    Serial.println(server.arg("brightness"));

    sendStr += ", hex:";
    sendStr += server.arg("hex");
    sendStr += ", brightness:";
    sendStr += server.arg("brightness");
  }
  
  server.send(200, "text/plain", sendStr);
}

void effect() {
  if(server.hasArg("effect")) {
    Serial.print(server.arg("effect"));

    currentEffect = (int)effect;

    if (effect == 0) {
      effectsEnabled = false;
    }
    else {
      effectsEnabled = true;
    }
  }

  server.send(200, "text/plain", "At effect: send 'none' to stop!");
}

void notFound() {
  server.send(200, "text/plain", "request not available");
}

void runEffect(int currentEffect) {
  switch (currentEffect) {
//    case 0: // should never actually run into this case, but just in _case_
//      return
    case 1:
      fade();
    case 2:
      rgbFade();
    case 3:
      strobe();
    case 4:
      runnin();
    case 5:
      colorWipe();
    case 6:
      rainbowCycle();
    case 7:
      fire();
    case 8:
      meteorRain();
  }  
  server.send(200, "text/plain", "running effect");
}

void loop() {
  server.handleClient();
  if(effectsEnabled) {
    runEffect(currentEffect);
  }
}
