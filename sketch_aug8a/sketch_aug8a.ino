#include <Servo.h>
Servo esc;
int pot;

void setup() {
  esc.attach(9, 1000, 2000);

  // Perform ESC calibration
  esc.writeMicroseconds(2000); // Send maximum pulse width
  delay(2000); // Wait for 2 seconds (you might need to adjust this)
  esc.writeMicroseconds(1000); // Send minimum pulse width
  delay(2000); // Wait for 2 seconds (you might need to adjust this)
}

void loop() {
  // for (int i = 0; i <= 100; i++) {
  //   pot = map(i, 0, 100, 0, 180);
  //   esc.write(pot);
  //   delay(100);
  // }
  pot = map(100, 0, 100, 0, 180);
    esc.write(pot);
    delay(100);
}
