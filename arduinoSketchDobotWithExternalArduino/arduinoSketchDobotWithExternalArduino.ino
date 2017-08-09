/*
** demo that dobot controled by another Arduino MEGA 2560
** with dobot firmware V1.2.0
** 
** connections:
** dobot side(Wireless port) | another Arduino side(UART1 port)
** GND ------ GND
** TX ------ TX1
** RX ------ RX1
** note: if another Arduino is self powered by USB or 12V, just connect above 3 lines is OK
** if another Arduino has no USB or 12V power, another connection between VCC ------ 5V is needed.
**
** 20160523
*/

static float cmd_str_10[10];
static unsigned char cmd_str_42[42];

// Send a 42 byte data packet to the dobot according to the communication protocol.
void cmd_str_42_send()
{
cmd_str_42[0] = 0xA5;
for( char i = 0; i < 10; i++ )
{
* ((float *)(cmd_str_42 + 1 + 4 *i)) = float( cmd_str_10[i] );
}
cmd_str_42[41] = 0x5A;

for( char i = 0; i < 42; i++ )
{
Serial1.write( cmd_str_42[i] );
}
}

//Set parameters of Dobot with state 9.
void dobot_cmd_3( int axis= 0, int Joint_jog_speed=0, int Joint_jog_acc=0){
for( char i = 0; i < 10; i++ ){
cmd_str_10[i] = 0;
}
// refer to protocal file for detail
cmd_str_10[0] = 9;
cmd_str_10[1] = axis; 
cmd_str_10[2] = Joint_jog_speed; 
cmd_str_10[3] = Joint_jog_acc; 
cmd_str_42_send();
}

//Set joint jog mode with state 2.
void dobot_cmd_2( int axis= 0, int StartVe= 0 ){
for( char i = 0; i < 10; i++ ){
cmd_str_10[i] = 0;
}
// refer to protocal file for detail
cmd_str_10[0] = 2;
cmd_str_10[1] = axis; 
cmd_str_10[7] = StartVe; 
cmd_str_42_send();
}

void setup() {
// put your setup code here, to run once:
// Serial1 connected with dobot
Serial1.begin(9600);
}

void loop() {
// put your main code here, to run repeatedly:
// wait dobot init...
delay( 1000 );
dobot_cmd_2( 0,0); // button released
dobot_cmd_3( 0,50,100); //configure the joint jog speed and the joint jog acceleration before controlling the dobot to move.

// move 3 loop
for( char i = 0; i < 2; i++ ){
dobot_cmd_2( 3,50); // joint1+(CCW)
// here just delay a few time between two cmd send simply
// for better performance, next cmd can be send out if a new frame on rxd is received
delay(1000); 
dobot_cmd_2( 0,0);// button released
delay(1000); //decelerate
dobot_cmd_2( 4,50);//joint1-(CW)
delay(1000);
dobot_cmd_2( 0,0);// button released
delay(1000); //decelerate
}

//end
while(1);
}
