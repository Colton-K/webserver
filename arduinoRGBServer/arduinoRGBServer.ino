// webserver vars
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define WIFI_SSID "thinkAP"
#define WIFI_PASS "penguinPinapplePizza"
ESP8266WebServer server(80);

// led vars
#include "FastLED.h"
#define NUM_LEDS 300
#define DATA_PIN 0
#define LED_TYPE WS2812B
CRGB leds[NUM_LEDS];

int r = 0, g = 0, b = 0;
int brightness = 0;
bool effectsEnabled = false;
int currentEffect = 0; // look at effects in switch case statement below

// for strobe
int strobeCount = 10;
int flashDelay = 50;
int endPause = 1000;
// for running
int waveDelay = 5;
// for colorWipe
int speedDelay = 5;
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
//  for(int i = 0; i < NUM_LEDS; i++ ) {
//    setPixel(i, red, green, blue);
//  }
//  FastLED.show();
  fill_solid(leds, NUM_LEDS, CRGB(red, green, blue));
}

/*
 * Prototypes
 */
void fade();
void rgbFade();
void strobe();
void runnin();
void colorWipe();
void rainbowCycle();
void fire();
void meteorRain();


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
  server.on("/test", test);
  server.onNotFound(notFound);
  server.begin();
  Serial.println("HTTP server started");

  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
//  FastLED.setBrightness(96);
  
  Serial.println("Leds initialized!");
}

void root() {
  server.send(200, "text/plain", "On root page");
}

void test() {
  server.send(200, "text/plain", "Starting test page!");

//  fill_solid(leds, NUM_LEDS, CRGB(0,255,0));
  setAll(255,0,255);
  FastLED.show();

}

void rgb() {
  String sendStr = "on rgb page";
  if(server.hasArg("r") && server.hasArg("g") && server.hasArg("b")) {


    r = server.arg("r").toInt();
    g = server.arg("g").toInt();
    b = server.arg("b").toInt();

    Serial.print(r);
    Serial.print(" ");
    Serial.print(g);
    Serial.print(" ");
    Serial.println(b);
    
    setAll(r, g, b);
    FastLED.show();
  }
  
  server.send(200, "text/plain", sendStr);
}

void effect() {
  String returnString = "At effect: ";
  if(server.hasArg("effect")) {

    currentEffect = server.arg("effect").toInt();

    returnString += "received ";
    returnString += currentEffect;
    returnString += " ";
    
    Serial.println(currentEffect);
    if (currentEffect == 0) {
      effectsEnabled = false;
    }
    else {
      effectsEnabled = true;
    }
  }

  returnString += "send 0 to stop!";
  server.send(200, "text/plain", returnString);
}

void notFound() {
  server.send(200, "text/plain", "request not available");
}

void runEffect(int currentEffect) {
  switch (currentEffect) {
    Serial.print("running effect: ");
    Serial.println(currentEffect);
    case 1:
      fade();
      return;
    case 2:
      rgbFade();
      return;
    case 3:
      strobe();
      return;
    case 4:
      runnin();
      return;
    case 5:
      colorWipe();
      return;
    case 6:
      rainbowCycle();
      return;
    case 7:
      fire();
      return;
    case 8:
      meteorRain();
      return;
    case 0: // should never actually run into this case, but just in _case_
      return;
  }  
}

void loop() {
  server.handleClient();
  if(effectsEnabled) {
    Serial.print("Effects are enabled, selected is: ");
    Serial.println(currentEffect);
    runEffect(currentEffect);
  }
}





void smartdelay(int t) {
  for(int i = 0; i < t; i++) {
    server.handleClient(); // will finish current effect, but at least update the webpage accordingly
    delay(t); 
  }
}

/*
 * EFFECTS
 */
 void fade() {
//  Serial.println("in fade");
  float red, green, blue;
     
  for(int k = 0; k < 256; k=k+1) {
    red = (k/256.0)*r;
    green = (k/256.0)*g;
    blue = (k/256.0)*b;
    setAll(red,green,blue);
    FastLED.show();
    delay(.1);
  }
//  smartdelay(.1);
     
  for(int k = 255; k >= 0; k=k-2) {
    r = (k/256.0)*red;
    g = (k/256.0)*green;
    b = (k/256.0)*blue;
    setAll(r,g,b);
    FastLED.show();
    delay(.1);
  }
//  smartdelay(.1);

  return;
}

void rgbFade() {
//  Serial.println("in rgbFade");

  for(int j = 0; j < 3; j++ ) {
    // Fade IN
    for(int k = 0; k < 256; k++) {
      switch(j) {
        case 0: setAll(k,0,0); break;
        case 1: setAll(0,k,0); break;
        case 2: setAll(0,0,k); break;
      }
      FastLED.show();
      delay(.1);
    }
    smartdelay(.1);
    // Fade OUT
    for(int k = 255; k >= 0; k--) {
      switch(j) {
        case 0: setAll(k,0,0); break;
        case 1: setAll(0,k,0); break;
        case 2: setAll(0,0,k); break;
      }
      FastLED.show();
      delay(.1);
    }
    smartdelay(.1);
  }

  return;
}

void strobe() {
//  Serial.println("in strobe");
  
  for(int j = 0; j < strobeCount; j++) {
    setAll(r, g, b);
    FastLED.show();
    delay(flashDelay);
    setAll(0,0,0);
    FastLED.show();
    delay(flashDelay);
  }
 
// smartdelay(endPause);
  smartdelay(.5);

 return;
}

void runnin() {
//  Serial.println("in running lights");
  
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
      smartdelay(waveDelay);
  }

  return;
}

void colorWipe() {
//  Serial.println("in colorWipe");
  
  for(uint16_t i=0; i<NUM_LEDS; i++) {
      setPixel(i, 0, 0, 0);
      FastLED.show();
      delay(speedDelay);
  }
//  smartdelay(.1);

  for(uint16_t i=0; i<NUM_LEDS; i++) {
      setPixel(i, r, g, b);
      FastLED.show();
      delay(speedDelay);
  }
  smartdelay(.1);

  return;
}
byte * Wheel(byte WheelPos) { // for rainbowCycle
  static byte c[3];
 
  if(WheelPos < 85) {
   c[0]=WheelPos * 3;
   c[1]=255 - WheelPos * 3;
   c[2]=0;
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   c[0]=255 - WheelPos * 3;
   c[1]=0;
   c[2]=WheelPos * 3;
  } else {
   WheelPos -= 170;
   c[0]=0;
   c[1]=WheelPos * 3;
   c[2]=255 - WheelPos * 3;
  }

  return c;
}
void rainbowCycle() {
  byte *c;
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< NUM_LEDS; i++) {
      c=Wheel(((i * 256 / NUM_LEDS) + j) & 255);
      setPixel(i, *c, *(c+1), *(c+2));
    }
    FastLED.show();
    smartdelay(speedDelay);
  }
  return;
}

void fire() {
//  Serial.println("in fire");

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

  return;
}

void meteorRain() {
//  Serial.println("in meteorRain");

  byte red = 0xff;
  byte green = 0xff;
  byte blue = 0xff;
  byte meteorSize = 10;
  byte meteorTrailDecay = 64;
  boolean meteorRandomDecay = true;
  int speedDelay = 10;
  
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

  return;
}
