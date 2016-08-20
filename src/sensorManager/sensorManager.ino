/*
 * 
 * Arduino script.
 * This script will automatically change screen brightness based on data received by the photoresistor connected to the Arduino board. It MUST be run as root!
 * 
 * Author: DaniLibe
 * Github: https://github.com/DaniLibe
 * Twitter: https://twitter.com/danilibe98
 * Mail: danylibedev@gmail.com
 *
 * If you find a bug contact me on danylibedev@gmail.com
 * Enjoy! ;)
 * 
*/

const int sensor_pin = A0;
int sensor_data;
int sensor_data_prev;

void setup()
{
  Serial.begin(9600); // It initializes the serial communication 

  sensor_data = analogRead(sensor_pin);
  Serial.println((String)sensor_data + "!");  // It gets the first read sensor value and prints It
}

void loop()
{
  // Data collection

  sensor_data_prev = sensor_data; // It gets a previous value of the sensor

  sensor_data = analogRead(sensor_pin);  // It gets the current value of the sensor

  if ((sensor_data >= (sensor_data_prev + 25)) || (sensor_data <= (sensor_data_prev - 25))) // If there is a difference of 25 between the current value and the previous one It sends the first (current sensor value)
  {
    Serial.println((String)sensor_data + "!");
  }

  delay(100); // It refreshes every hundredth of a second
}
