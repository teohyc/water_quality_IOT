const int NUM_SENSORS = 3;
const int NUM_SAMPLES = 10;
const unsigned long SAMPLE_INTERVAL = 3000; // 3 seconds

// Analog pins
int sensorPins[NUM_SENSORS] = {A0, A1, A2};

// Storage for samples
int samples[NUM_SENSORS][NUM_SAMPLES];
int sampleIndex = 0;

unsigned long lastSampleTime = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial to be ready

  Serial.println("Arduino Water Quality Sensor Started");
}

void loop() {
  unsigned long currentTime = millis();

  // Take sample every 3 seconds
  if (currentTime - lastSampleTime >= SAMPLE_INTERVAL) {
    lastSampleTime = currentTime;

    // Read all sensors
    for (int i = 0; i < NUM_SENSORS; i++) {
      samples[i][sampleIndex] = analogRead(sensorPins[i]);
    }

    sampleIndex++;

    // If 10 samples collected (30 seconds)
    if (sampleIndex >= NUM_SAMPLES) {
      sendAverages();
      sampleIndex = 0; // Reset for next window
      
    }
  }
}

void sendAverages() {
  float averages[NUM_SENSORS];

  // Compute average for each sensor
  for (int i = 0; i < NUM_SENSORS; i++) {
    long sum = 0;
    for (int j = 0; j < NUM_SAMPLES; j++) {
      sum += samples[i][j];
    }
    averages[i] = (float)sum / NUM_SAMPLES;
  }

  // Send via Serial (USB)
  Serial.print("AVG,");
  Serial.print(averages[0]);
  Serial.print(",");
  Serial.print(averages[1]);
  Serial.print(",");
  Serial.println(averages[2]);
}