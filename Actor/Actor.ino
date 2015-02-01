
#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"
#include <Servo.h> 
#include <CmdMessenger.h>  // CmdMessenger                                            //--------------- includes

#define BAUD_RATE 115200

#define BUTTON_PIN 11

#define BUS_PIN 9            //on this, the servo is attached
#define BUS_TOGGLE_PIN 12     //the signal to the transistor to control the power used by the servo
#define BUS_DRIVE_DELAY 100
#define BUS_0_POS 30          //it's not possible to set the bus on zero position 
#define BUS_100_POS 160       //the samo on its absolut position

#define DISPLAY_BRIGHTNESS 0
#define DISPLAY_CLEAR_SPEED 30
#define DISPLAY_TEXT_SPEED 50                                                        //------------------ constances


//a little 8x8 matrix represents a display
Adafruit_8x8matrix _display = Adafruit_8x8matrix();

//controller of the little magnet > bus-figure
//it's a servo motor attached with a magnet
//the magnet sweeps under the painted street (between 0 to 180 degree)
Servo _busServo;  
int _curBusPos = 100;  

//error feedback is just a simple error string
String _errorMsg;

// Attach a new CmdMessenger object to the default Serial port
CmdMessenger _cmdMessenger = CmdMessenger(Serial);
//Commands
enum{
  writeText,       //Command to write a text in matrix
  writeNumber,     //Command to write a number in matrix
  drawImage,       //Command to draw a 8x8 picture
  clearDisplay,    //Command to clear the current display
  setBusPosition,   //Command to set bus on a specific position
  getButtonState,  //Command to get Button state
  getError,         //Command to get errors if there
  
  sendButtonState,  //Command to send the button state
  sendError         //Command to send the current error
};                                                                                  //----------------- globals

// Callbacks define on which received commands we take action 
void AttachCommandCallbacks()
{
  _cmdMessenger.attach(OnUnknownCommand);
  _cmdMessenger.attach(writeText, OnWriteText);
  _cmdMessenger.attach(writeNumber, OnWriteNumber);
  _cmdMessenger.attach(drawImage, OnDrawImage);
  _cmdMessenger.attach(clearDisplay, OnClear);
  _cmdMessenger.attach(setBusPosition, OnDriveBus);
  _cmdMessenger.attach(getButtonState, OnGetButtonState);
  _cmdMessenger.attach(getError, OnSendError);
}

void setupDisplay()
{
  //define the display
  _display.begin(0x70);  // pass in the address
  _display.setRotation(2);    //i stick it the wrong way up, so we have to turn it at the beginning
  _display.setBrightness(DISPLAY_BRIGHTNESS);  //it shouldn't blend
  _display.clear();
  _display.writeDisplay();
}

void setupBus()
{
  //define the servo of the bus
  _busServo.attach(BUS_PIN);  // attaches the servo on pin BUS_PIN to the servo object 
  delay(500);
  for(int i = BUS_100_POS; i >= BUS_100_POS-5; i--)
  {
        _busServo.write(i);
        delay(30);
  }
  for(int i = BUS_100_POS-5; i <= BUS_100_POS; i++)
  {
        _busServo.write(i);
        delay(30);
  }
  pinMode(BUS_TOGGLE_PIN, OUTPUT);
  digitalWrite(BUS_TOGGLE_PIN, HIGH);  //turn it off on startup
  _busServo.detach();
}

void setup() {
  
  // Listen on serial connection for messages from the pc
  Serial.begin(BAUD_RATE); 

  // Adds newline to every command
  _cmdMessenger.printLfCr();
  
  // Attach my application's user-defined callback methods
  AttachCommandCallbacks();
  
  //define the input-button
  pinMode(BUTTON_PIN, INPUT);

  _errorMsg = "";
  //set the bus at start position
  //SetBusOnStart();
                                                                                            
  setupDisplay();
  setupBus();
}                                                                                          //--------------- setup


//a method to write a text on the 8x8-pixel-matrix (_display)
//automaticaly scrolling!
//  text :  String, to write
//  stay : Boolean, to turn on/off a automatic scrolling loop of the text
//  pos : Int, Offset to write the text
void OnWriteText()                                                                                    //onWriteText
{
  String text = _cmdMessenger.readStringArg();
  boolean stay = _cmdMessenger.readBoolArg();
  int pos = _cmdMessenger.readInt32Arg();
  
  _display.setTextSize(1);
  _display.setTextWrap(false);  // we dont want text to wrap so it scrolls nicely
  _display.setTextColor(LED_ON);
  if(!stay)
  {
    int length = text.length();
    OnClear();
    for (int8_t x=pos; x>=-(length*6); x--) {
        _display.clear();
        _display.setCursor(x,0);
        _display.print(text);
        _display.writeDisplay();
        delay(DISPLAY_TEXT_SPEED);
      }
  }
  else
  {
    OnClear();
    _display.setCursor(pos,0);
    _display.print(text);
    _display.writeDisplay();     
  }
}

//a method to write a number on the 8x8-pixel-matrix (_display)
//  num : Int, the number to draw (should be less than 20 to fit on the screen, otherwise it scrolls!)
void OnWriteNumber()
{
  int num = _cmdMessenger.readInt32Arg();                                                              //OnWriteNumber
  int decPos = 3;
  OnClear();
  _display.clear();
  if(num < 10)
  {
      _display.setCursor(decPos,1);
      _display.print(num);
      _display.writeDisplay();
  }
  else if(num < 20)
  {
      _display.drawLine(1,3, 1,7, LED_ON);
      _display.drawLine(1,3, 0,4, LED_ON);
      _display.setCursor(decPos,1);
      _display.print(num-10);
      _display.writeDisplay();
  }
  else if(num < 30)
  {
      _display.drawPixel(0,3, LED_ON);
      _display.drawLine(1,3, 1,5, LED_ON);
      _display.drawLine(0,5, 0,7, LED_ON);
      _display.drawPixel(1,7, LED_ON);
      _display.setCursor(decPos,1);
      _display.print(num-20);
      _display.writeDisplay();
  }
  else if(num < 40)
  {
      _display.drawPixel(0,2, LED_ON);
      _display.drawLine(1,3, 1,3, LED_ON);
      _display.drawPixel(0,4, LED_ON);
      _display.drawLine(1,5, 0,7, LED_ON);
      _display.drawPixel(0,7, LED_ON);
      _display.setCursor(decPos,1);
      _display.print(num-30);
      _display.writeDisplay();
  }
  else 
  {
      _display.setTextWrap(false);
      String numText = String(num);
      int length = numText.length();
      for (int8_t x=0; x>=-(length*6); x--) {
        _display.clear();
        _display.setCursor(x,0);
        _display.print(numText);
        _display.writeDisplay();
        delay(DISPLAY_TEXT_SPEED);
      }
  }
}

//a method to draw an 8x8 image on the matrix (_display)
//   image: int[7], numbers wich represents a 8-bit-value / the eight rows 
//  withClear : Decision if the _displey should be cleared befor drawing
//   showComplete : Decision if the image should slide in or blink on
void OnDrawImage()                                                                                  //OnDrawImage
{
  int image[] = {_cmdMessenger.readInt32Arg(),
                _cmdMessenger.readInt32Arg(),
                _cmdMessenger.readInt32Arg(),
                _cmdMessenger.readInt32Arg(),
                _cmdMessenger.readInt32Arg(),
                _cmdMessenger.readInt32Arg(),
                _cmdMessenger.readInt32Arg(),
                _cmdMessenger.readInt32Arg()};
  boolean withClear = _cmdMessenger.readBoolArg();
  boolean showComplete = _cmdMessenger.readBoolArg();
  if(withClear)
    Clear(false);
  for(int row = 0; row < 8; row++)
  {
     for(int col = 0; col < 8; col++)
     {
       boolean pixVal = bitRead(image[row], col);
       _display.drawPixel(col, row, pixVal);
       if(withClear)
         _display.drawPixel(col, row+1, LED_ON);
     }
     if(!showComplete)
     {
       _display.writeDisplay();
       delay(DISPLAY_CLEAR_SPEED);
      }
  }
  if(showComplete)
    _display.writeDisplay();
}

//a method to clear the 8x8-pixel-matrix (_display)
//  flag : Boolean, clear it with on- or off-pixels
void OnClear()                                                                                      //OnClear
{
  boolean flag = _cmdMessenger.readBoolArg();
  for(int row = 0; row < 11; row ++)
  {
    for(int i = 0; i < 8; i++)
    {
        if(row > 0)
        {
            _display.drawPixel(i, row-1, flag);
        }
        if(row < 9)
          _display.drawPixel(i, row, !flag);
    }
    _display.writeDisplay();
    delay(DISPLAY_CLEAR_SPEED);
  }  
}

void Clear(boolean flag)
{
  for(int row = 0; row < 11; row ++)
  {
    for(int i = 0; i < 8; i++)
    {
        if(row > 0)
        {
            _display.drawPixel(i, row-1, flag);
        }
        if(row < 9)
          _display.drawPixel(i, row, !flag);
    }
    _display.writeDisplay();
    delay(DISPLAY_CLEAR_SPEED);
  }  
}

//a method to drive the bus to a percentual position of its half circle
//  pos : Int (0 - 100), percentual position
void OnDriveBus()                                                                                  //OnDriveBus
{
    int pos = _cmdMessenger.readInt32Arg();
    //_busServo.write(pos);
    //return;
    if(pos < 0 || pos > 100 || pos == _curBusPos)
      return;
    _busServo.attach(BUS_PIN);
    delay(500);
    if(pos > _curBusPos)
    {
        for(int i = _curBusPos; i <= pos; i++)
        {
            _busServo.write(GetBusAngle(i));
            delay(BUS_DRIVE_DELAY);
        }
    }
    else
    {
        for(int i = _curBusPos; i >= pos; i--)
        {
            _busServo.write(GetBusAngle(i));
            delay(BUS_DRIVE_DELAY);
        }
    }
    _curBusPos = pos;
    Serial.println(pos);
    _busServo.detach();
}

int GetBusAngle(int percentage)
{
  if(percentage == 0) return BUS_0_POS;
   float angle = (BUS_100_POS - BUS_0_POS)*((float)percentage/100);
   return (int)(angle + BUS_0_POS);
}

//a method to request the current button state
void OnGetButtonState()                                                                            //OnGetButtonState
{
    boolean buttonState = digitalRead(BUTTON_PIN);
    _cmdMessenger.sendCmd(sendButtonState,buttonState);
}

// Called when a received command has no attached function
void OnUnknownCommand()                                                                            //OnUnknownCommand
{
  _cmdMessenger.sendCmd(sendError,"Command without attached callback");
}

//a method to request the current error message
void OnSendError()                                                                                //OnSendError
{
  _cmdMessenger.sendCmd(sendError,_errorMsg);
}

void loop() {
  // Process incoming serial data, and perform callbacks
  _cmdMessenger.feedinSerialData();
}


