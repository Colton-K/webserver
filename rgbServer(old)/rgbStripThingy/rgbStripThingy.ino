const int redPin = 6;
const int greenPin = 3;
const int bluePin = 9;

const char redStart = '<';
const char redStop   = '>';
const char greenStart   = '-';
const char greenStop   = '_';
const char blueStart = '(';
const char blueStop = ')';
const char effectStart = '*';
const char effectStop = '^';

bool fading = false;
bool specialFading = false;
bool strobing = false;

bool controllerConnected = false;
char receivedChar;

int r = 0;
int g = 0;
int b = 0;

void setup() {
  Serial.begin(9600);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void setLED(int pin, const long n) {
  Serial.print("Setting pin ");
  Serial.print(pin);
  Serial.print(" to ");
  Serial.println(n);

  analogWrite(pin, n);
}

void setAll(int r, int g, int b) {
  setLED(redPin, r);
  setLED(greenPin, g);
  setLED(bluePin, b);
}

// fancy programs
void fade() {
  for (int j = 0; j < 3; j++ ) {
    // Fade IN
    for (int k = 0; k < 256; k++) {
      switch (j) {
        case 0: setAll(k, 0, 0); break;
        case 1: setAll(0, k, 0); break;
        case 2: setAll(0, 0, k); break;
      }
      delay(3);
    }
    // Fade OUT
    for (int k = 255; k >= 0; k--) {
      switch (j) {
        case 0: setAll(k, 0, 0); break;
        case 1: setAll(0, k, 0); break;
        case 2: setAll(0, 0, k); break;
      }
      delay(3);
    }
  }
}

void fade(byte red, byte green, byte blue, int delayDuration) {
  float r, g, b;

  for (int k = 0; k < 256; k = k + 1) {
    r = (k / 256.0) * red;
    g = (k / 256.0) * green;
    b = (k / 256.0) * blue;
    setAll(r, g, b);
    delay(delayDuration);
  }

  for (int k = 255; k >= 0; k = k - 2) {
    r = (k / 256.0) * red;
    g = (k / 256.0) * green;
    b = (k / 256.0) * blue;
    setAll(r, g, b);
    delay(delayDuration);
  }
}

void Strobe(byte red, byte green, byte blue, int StrobeCount, int FlashDelay, int EndPause) {
  for (int j = 0; j < StrobeCount; j++) {
    setAll(red, green, blue);
    delay(FlashDelay);
    setAll(0, 0, 0);
    delay(FlashDelay);
  }

  // delay(EndPause);
}

void processInput()
{
  static long receivedRed = 0;
  static long receivedGreen = 0;
  static long receivedBlue = 0;
  static long receivedEffect = 0;

  byte c = Serial.read();

  switch (c)
  {
    case redStop:
      r = receivedRed;
      setLED(redPin, receivedRed);
      break;

    // fall through to start a new number
    case redStart:
      receivedRed = 0;
      break;

    case '0' ... '9':
      receivedRed *= 10;
      receivedRed += c - '0';
      break;
  }

  switch (c)
  {
    case greenStop:
      g = receivedGreen;
      setLED(greenPin, receivedGreen); // play with the negative sign!
      break;

    // fall through to start a new number
    case greenStart:
      receivedGreen = 0;
      break;

    case '0' ... '9':
      receivedGreen *= 10;
      receivedGreen += c - '0';
      break;
  }

  switch (c)
  {
    case blueStop:
      b = receivedBlue;
      setLED(bluePin, receivedBlue); // play with the negative sign!
      break;

    // fall through to start a new number
    case blueStart:
      receivedBlue = 0;
      break;

    case '0' ... '9':
      receivedBlue *= 10;
      receivedBlue += c - '0';
      break;
  }

  switch (c)
  {
    case effectStop:
      if (receivedEffect == 404) {
        Serial.println("rgbStripController");
      }
      else if (receivedEffect == 0) {
        Serial.println("no effect");
        fading = false;
        specialFading = false;
        strobing = false;
      }
      else if (receivedEffect == 1) {
        Serial.println("fading");
        fading = !fading;
      }
      else if (receivedEffect == 2) {
        Serial.println("special fading");
        specialFading = !specialFading;
      }
      else if (receivedEffect == 3) {
        Serial.println("strobing");
        strobing = !strobing;
      }
      break;

    case effectStart:
      receivedEffect = 0;
      break;

    case '0' ... '9':
      receivedEffect *= 10;
      receivedEffect += c - '0';
      break;
  }
}

void connectToPi() {
  Serial.println("rgbStripThingy");
  if (Serial.available() > 0) {
    receivedChar = Serial.read();

    if (receivedChar == 'y') {
      controllerConnected = true;
    }
  }
}

void loop() {
  if (controllerConnected) {
    if (Serial.available() > 0) {
      processInput();
    }
  }
  else {
    connectToPi();
  }
  if (fading) {
    //      fade(0xff, 0x77, 0x00, 3);
    fade();
    processInput();
  }
  if (specialFading) {
    fade(r, g, b, 6);
    processInput();
  }
  if (strobing) {
    Strobe(r, g, b, 1, 40, 1000);
    processInput();
  }
}
