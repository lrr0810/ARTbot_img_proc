#include <RH_NRF24.h>
#include <stdio.h>
#include <stdlib.h>

void setup() {
  // put your setup code here, to run once:
  // CAUTION: Pins 5 & 6 have higher actual PWM output

  // Defined set of GPIO pins for left & right sides
  #define PWM_left(){
    pin[0] = 3;
    pin[1] = 5;
    pin[2] = 9;
  }

  #define PWM_left(){
    pin[0] = 6;
    pin[1] = 10;
    pin[2] = 11;
  }

#define M1_speed = 0
#define M2_speed = 0
 
}

void loop() {
  // put your main code here, to run repeatedly:
  // TODO: add channel that cx will be sent from 

  // TODO: write in code that actually works for reading value from radio
  //radio.read(cx)
  //
  
  int i = 0;

  void set_side (side, value){
    if (side == 'left'){
      for (i = 0; 1 < 3; i++){
        PWM_left.pin[i] = value;
      }
    }

    else if (side == 'right'{
      for (i = 0; 1 < 3; i++){
        PWM_right.pin[i] = value;
      }
    }

  void direction_set(cx){

    //left case
     if (cx <= 150){
         setM1Speed(100);
         setM2Speed(300);
      }

      //straight case
      else if (cx >151 && cx < 169){
        setM1Speed(300);
        setM2Speed(300);
      }

      //Right case
      else if (cx >151 && cx < 169){
        setM1Speed(300);
        setM2Speed(100);
      }
    }
  }



}
