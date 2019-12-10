#include<Wire.h>
#include<SoftwareSerial.h>
SoftwareSerial mySerial(3, 4); // RX, TX

#define MPU6050 0x68 //MPU 6050 의 I2C 기본 주소 설정
#define X_ERROR 10
#define Y_ERROR 10
#define X_RANGE 10
#define Y_RANGE 10
#define COUNT_REFRESH 20
#define END_NUMBER 30
#define POWER_LED 13
#define WORK_LED 12

//------------------------------------------------------------------------------------------------------
int16_t AcX, AcY, AcZ;
int16_t AcZ_X=12700, AcZ_Y=12800;
int x_final, y_final;
int x_origin = 0, y_origin = 0;
int x_range = 0, y_range = 0;
int Save_Number = 0;
int Final_Number = 0;
int count_refresh = 0;
int count_number = 0;
uint8_t ud_flag;
uint8_t startdown_flag = 0;
uint8_t Start_Flag = 0;
int Flag_IR = 0;
int Recive_Erorr_flag = 0;
String msg = "";
int Final_Number_Save = 0;
//------------------------------------------------------------------------------------------------------
/*--User Define Funtion--*/
void mpu6050_Read(void);
void mpu6050_analysis(void);
int mpu6050_x_correction(double);
int mpu6050_y_correction(double);
void cube_startdown(void);
void cube_save_number(void);
void cube_final_number(void);
void Send_msg(void);
void CKIN(void);

void debug_print(void);
//------------------------------------------------------------------------------------------------------
void mpu6050_Read()
{
  Wire.beginTransmission(MPU6050);    //데이터 전송시작
  Wire.write(0x3B);               // register 0x3B (ACCEL_XOUT_H), 큐에 데이터 기록
  Wire.endTransmission(false);    //연결유지
  Wire.requestFrom(MPU6050,6,true);   //MPU에 데이터 요청 

  //데이터 한 바이트 씩 읽어서 반환
  AcX = Wire.read() << 8 | Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY = Wire.read() << 8 | Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read() << 8 | Wire.read();
}
//------------------------------------------------------------------------------------------------------
void mpu6050_analysis()
{
  double RADIAN_TO_DEGREES = 180/3.14;
  double x_vlaue = atan(AcY/sqrt(pow(AcX,2) + pow(AcZ_X,2))) * RADIAN_TO_DEGREES; //보정전 Roll값 구하기
  double y_vlaue = atan(AcX/sqrt(pow(AcY,2) + pow(AcZ_Y,2))) * RADIAN_TO_DEGREES; //보정전 Pitch값 구하기 
  x_final = mpu6050_x_correction(x_vlaue);
  y_final = mpu6050_y_correction(y_vlaue);

  if(AcZ < -15000)
  {
   ud_flag = 1; 
  }
  else
  {
    ud_flag = 0; 
  }
}
//------------------------------------------------------------------------------------------------------
int mpu6050_x_correction(double x_vlaue)
{
  x_vlaue = floor(x_vlaue+0.5);  //x_vlaue값 보정
  x_vlaue += 52;             //x_vlaue값의 음수값 삭제  

  double x_final = 90.0/104.0*x_vlaue;

  if(x_final == 45)
  {
    x_final = 0;
  }
  
  else if(x_final > 45)
  {
    if(x_final > 90)
    {
      x_final = -90;
    } 
    else
    {
      x_final -= 46; 
      x_final = 90.0/44.0*x_final;
      x_final *= -1;
    }
  }
  
  else if(x_final < 45)
  {
    if(x_final < 0)
    {
      x_final = 90;
    }
    else
    {
      x_final = 90.0/44.0*x_final-90;
      x_final *= -1;
    }
  }
   x_final = int(x_final);
   
   return x_final; 
}
//------------------------------------------------------------------------------------------------------
int mpu6050_y_correction(double y_vlaue)
{
  y_vlaue = floor(y_vlaue);  //y_vlaue값 보정
  y_vlaue += 52;         //y_vlaue값의 음수값 삭제

  double y_final = 90.0/104.0*y_vlaue;
  
  if(y_final == 45)
  {
    y_final = 0;
  }
  
  else if(y_final > 45)
  {
    if(y_final > 90)
    {
      y_final = 90;
    }

    else
    {
      y_final -= 46; 
      y_final = 90.0/44.0*y_final;
    }
  }
  
  else if(y_final < 45)
  {
    if(y_final < 0)
    {
      y_final = -90;
    }

    else
    {
      y_final = 90.0/44.0*y_final-90;
    }
  }
   y_final = floor(y_final);
   
   return y_final; 
}
//------------------------------------------------------------------------------------------------------
void cube_startdown()
{
  if(count_refresh == COUNT_REFRESH)
  {
    x_range = x_origin - x_final;
    y_range = y_origin - y_final;
    
    if(x_range < 0)
    {
      x_range *= -1;
    }
    if(y_range < 0)
    {
      y_range *= -1;
    }    

    if(x_range >= X_RANGE || y_range >= Y_RANGE)
    {
      startdown_flag = 1;
    }
    else
    {
      x_origin = x_final;
      y_origin = y_final;
    }
    count_refresh = 0;
  }
  else
  {
    count_refresh++;
  }
}
//------------------------------------------------------------------------------------------------------
void cube_save_number()
{
  if(ud_flag != 1)
  {
    if(x_final >= 90-X_ERROR && x_final <= 90+X_ERROR)
    {
      if(y_final >= 0-X_ERROR && y_final <= 0+X_ERROR)
      {
        Save_Number = 2;
      }
    }

    else if(x_final >= -90-X_ERROR && x_final <= -90+X_ERROR)
    {
      if(y_final >= 0-X_ERROR && y_final <= 0+X_ERROR)
      {
        Save_Number = 5;
      }
    }

    else if(x_final >= 0-X_ERROR && x_final <= 0+X_ERROR)
    {
      if(y_final >= 90-X_ERROR && y_final <= 90+X_ERROR)
      {
        Save_Number = 3;
      }
      
      else if(y_final >= -90-X_ERROR && y_final <= -90+X_ERROR)
      {
        Save_Number = 4;
      }

      else if(y_final >= 0-X_ERROR && y_final <= 0+X_ERROR)
      {
        Save_Number = 1;
      }
    }
  }
  else
  {
    Save_Number = 6;
  }
}
//------------------------------------------------------------------------------------------------------
void cube_final_number()
{
    if(Final_Number == Save_Number)
    {
      count_number++;
    }
    else
    {
      Final_Number = Save_Number;
      count_number = 0;
    }
  
   if(count_number == END_NUMBER)
   {
      if(Final_Number == 0)
      {
        Final_Number = 7;   
      }
      Start_Flag = 0;
   } 
}
//------------------------------------------------------------------------------------------------------
void Send_msg()
{
 char temp;
  msg = "";
  Serial.println("in"); 
  while (mySerial.available())
  {
      //Serial.println(mySerial.available());
      //Serial.println(" Received something. \n\r");
      temp = mySerial.read();
      //Serial.println(temp);
      msg.concat(temp);
  }
   //Serial.println(msg);
  if (msg == "SEND PLESE")
  {
    x_origin = x_final;
    y_origin = y_final;
    
    while(startdown_flag == 0)
    {
      mpu6050_Read();
      mpu6050_analysis();
      cube_startdown();
      debug_print();
      delay(500);
    }
    cube_save_number();
    cube_final_number();
    debug_print();
    mySerial.write(48+Final_Number);
    Serial.println(48+Final_Number);
    Serial.println("OK"); 
    Final_Number_Save = Final_Number;
    Final_Number = 0;
    startdown_flag = 0;
    count_refresh = 0;
    count_number = 0;
    delay(500);
  }
  delay(200);

}
//------------------------------------------------------------------------------------------------------
void CKIN(){
  Flag_IR = 1;
}
//------------------------------------------------------------------------------------------------------
void debug_print(void)
{
   //시리얼 모니터에 출력
  Serial.print("x_final = "); Serial.println(x_final);
  Serial.print("y_final = "); Serial.println(y_final);
  Serial.print("ud_flag = "); Serial.println(ud_flag);
  Serial.print("Save_Number = "); Serial.println(Save_Number);
  Serial.print("x_origin = "); Serial.println(x_origin);
  Serial.print("y_origin = "); Serial.println(y_origin);
  Serial.print("x_range = "); Serial.println(x_range);
  Serial.print("y_range = "); Serial.println(y_range);
  Serial.print("count_refresh = "); Serial.println(count_refresh);
  Serial.print("Final_Number = "); Serial.println(Final_Number);
  Serial.print("count_number = "); Serial.println(count_number);
  Serial.print("msg = "); Serial.println(msg);
  
  Serial.println(" ");
}
//------------------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------
void setup()
{
  Wire.begin();      //Wire 라이브러리 초기화
  Wire.beginTransmission(MPU6050); //MPU로 데이터 전송 시작
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     //MPU-6050 시작 모드로 만들기
  Wire.endTransmission(true);
  Serial.begin(9600);
  while (!Serial) 
  {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  mySerial.begin(9600);
  mySerial.Registcallback(CKIN);
}
//------------------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------
void loop()
{
  mpu6050_Read();
  mpu6050_analysis();
  if(Flag_IR == 1)
  {
   Send_msg(); 
   Flag_IR = 0;
  }
  debug_print();
  delay(500);
}
