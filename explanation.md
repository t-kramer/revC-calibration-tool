Trying to calibrate the revC sensor against high-quality reference equipment, we found that the low-cost
revC anemometers showed a slight sensor-to-sensor error. This means that the sensors were not generating the same
raw output voltages under similar environmental conditions. Fortunately, we found that the observed error was relatively constant over the whole calibration range. This facilitates the calibration process.


For the calibration we analysed the correlation between the sensors raw RV and TMP outputs and velocity measurements made by reference equipment. We collected these measurements in a purpose-built, simple wind tunnel. We found that all sensors more or less correlate with the reference measurements in a similar way, following a function of the form f(RV,TMP) = beta_0xRV^3 + beta_1xTMP + b. While it should always be the preferred option to determine the specific coefficients *beta_0*, *beta_1* and *b* for each sensor individually (like we did), the constant error between sensors allows a simplified calibration process:


1. Connect your climateBOX/ESP32 incl. revC sensor to your computer/laptop via USB.
2. Let it go through one or two measurement cycles. The sensor needs some time to stabilise.
3. Open the Arduino IDE and use the serial monitor to observe the climateBOX readings.
4. After the warming-up period, use a paper cup to cover the revC sensor.
5. For at least two measurement cycles, keep the cup over the sensor and write down both the RawRVScale and RawTMPScale values.
6. Calculate the mean values for both variables.
7. Enter those values in the dedicated input fields below.
8. Take note of the zeroWind adjustment value for your sensor.
9. Update the zeroWindAdjustment variable in the your climateBOX code [LINK] and re-upload the program to your climateBOX unit.


*Note: You have to go through this process for every revC sensor you are using.*

 

By calibrating multiple sensors individually, we were able to find the 'mean curve' or reference function for all investigated sensors (dotted grey line below). In an ideal scenario, your sensors behaviour (black line) is very close to this reference function. Unfortunately, in most cases this is not true.


Covering the sensor with a paper cup creates a reference scenario of an air velocity of ~0.0 m/s. If you gather your raw RV and TMP values and use them as input for the reference function, you'll get an output in m/s. Because the sensor is covered, the reading should be around 0.0 m/s, right? If the value is significantly larger or smaller than 0.0, we need to account for this deviation and adjust the sensor measurements by the observed deviation. We call this deviation at 'zero Wind' *zeroWind adjustment*.


Here, based on our analysis, we can assume that this deviation is mostly constant over the full measurement range. This means that for the records the sensor is going to make, we use the reference function for conversion from raw voltage to m/s and then make use of the zeroWind adjustment to correct the deviation of our sensor.
