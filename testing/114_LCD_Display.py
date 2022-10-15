from machine import Pin,SPI,PWM
import framebuf
import time


BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.yellow =  0xF740
        self.black =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    
  
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    #color BRG
    LCD.fill(LCD.black)
 
    LCD.show()
    LCD.text("Open Slider v1.0",8,8,LCD.green)
    LCD.text("Demo",8,20,LCD.green)
    LCD.text("Pico-LCD-1.14",8,32,LCD.green)
 
    LCD.line(8,44,134,44,LCD.green)

    LCD.text("Count:", 8, 50, LCD.green)

    # LCD.hline(1,1,238,LCD.black)
    # LCD.hline(1,133,238,LCD.black)
    # LCD.vline(1,1,133,LCD.black)
    # LCD.vline(239,1,133,LCD.black)
    
    LCD.show()
    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)
    key4 = Pin(16 ,Pin.IN,Pin.PULL_UP)
    key5 = Pin(18 ,Pin.IN,Pin.PULL_UP)
    key6 = Pin(20 ,Pin.IN,Pin.PULL_UP)
    
    count = 0
    c1 = count
    
    while(1):
        
        if c1 > count:
            LCD.text(str(count), 60,50,LCD.black)
            LCD.show()
            LCD.text(str(c1), 60,50,LCD.green)
            LCD.show()
            count = c1
            print(count)
#        else:
#            LCD.text(f"Count: {c1}", 8,50,LCD.green)

        if(keyA.value() == 0):
            LCD.fill_rect(230,0,10,10,LCD.green)
            print("A")
        else :
            LCD.fill_rect(230,0,10,10,LCD.green)
            LCD.rect(230,0,10,10,LCD.green)
            
            
        if(keyB.value() == 0):
            LCD.fill_rect(228,125,10,10,LCD.green)
            print("B")
        else :
            LCD.fill_rect(228,125,10,10,LCD.green)
            LCD.rect(228,125,10,10,LCD.green)
    
    
    
    
        if(key2.value() == 0):
            c1 += 1
            LCD.fill_rect(17,93,10,10,LCD.red)
            print("UP")
        else :
            LCD.fill_rect(17,93,10,10,LCD.green)
            LCD.rect(17,93,10,10,LCD.green)
            
            
        if(key3.value() == 0):#中
            LCD.fill_rect(17,108,10,10,LCD.red)
            print("CTRL")
        else :
            LCD.fill_rect(17,108,10,10,LCD.green)
            LCD.rect(17,108,10,10,LCD.green)
            
        

        if(key4.value() == 0):#左
            LCD.fill_rect(2,108,10,10,LCD.red)
            print("LEFT")
        else :
            LCD.fill_rect(2,108,10,10,LCD.green)
            LCD.rect(2,108,10,10,LCD.green)
            
            
        if(key5.value() == 0):#下
            LCD.fill_rect(17,123,10,10,LCD.red)
            print("DOWN")
        else :
            LCD.fill_rect(17,123,10,10,LCD.green)
            LCD.rect(17,123,10,10,LCD.green)
            
            
        if(key6.value() == 0):#右
            LCD.fill_rect(32,108,10,10,LCD.red)
            print("RIGHT")
        else :
            LCD.fill_rect(32,108,10,10,LCD.green)
            LCD.rect(32,108,10,10,LCD.green)
    
        LCD.show()
        
    time.sleep(1)
    LCD.fill(0xFFFF)




