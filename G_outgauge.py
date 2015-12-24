import socket, os, time, struct, GLCD_SDK, math, ctypes, sys
from PIL import Image, ImageDraw,ImageFont
from threading import Thread


version = "0.0.1"
Servname = "OutGauge.py "+version

def log(blabla):
     os.chdir(os.getcwd())
     flog = open("data.log", "a")
     flog.write(blabla+"\n")
     flog.close()
     
def msg_error(txt):
     if getattr(sys, 'frozen', False):
        # The application is frozen
          ctypes.windll.user32.MessageBoxW(0, unicode(txt, "utf-8"), u"Error", 0x10)
          sys.exit(-1)
     else:
          raise Exception(txt)

class OutgaugeServer(Thread):
     """Outgauge UDP Server thread class"""
     
     def __init__(self, UDP_IP = "", UDP_PORT = 4444):
          Thread.__init__(self)
          self.work = True
          self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          
          sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          result = sock.connect_ex(('localhost',4444))
          if result == 0:
               print "Port is open"
          else:
               print "Port 4444 is not open (",result,')'
               msg_error("Application exit : Port is already used")
             
          self.sock.bind((UDP_IP, UDP_PORT))
          print "Serveur demarre a %s:%i"%(UDP_IP,UDP_PORT)
          self.time=0
          self.car=""
          self.words=""
          self.gear=1
          self.spareb=""
          self.speed=0.0 #M/S
          self.RPM=0.0
          self.turbo=0.0
          self.engtemp=0.0
          self.fuel=0.0
          self.oilpress=0.0
          #self.spare1=0.0
          #self.spare2=0.0
          #self.spare3=0.0
          self.throttle=0.0
          self.brake=0.0
          self.clutch=0.0
          self.display1=""
          self.display2=""
          self.dashlights=0
          self.showlights=0
          
     def run(self):
          while self.work:
               data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
               self.time= struct.unpack("I",data[:4])[0]
               self.car= data[4:8]
               self.words=struct.unpack("H",data[8:10])[0]
               self.gear=struct.unpack("H",data[10:12])[0]
               self.spareb=struct.unpack("H",data[12:14])[0]
               self.speed=struct.unpack("f",data[12:16])[0] #M/S
               self.RPM=struct.unpack("f",data[16:20])[0]
               self.turbo=struct.unpack("f",data[20:24])[0]
               self.engtemp=struct.unpack("f",data[24:28])[0]
               self.fuel=struct.unpack("f",data[28:32])[0]
               self.oilpress=struct.unpack("f",data[32:36])[0]
               self.dashlights =struct.unpack("I",data[44:48])[0]
               self.showlights =struct.unpack("I",data[40:44])[0]
               #self.spare3=struct.unpack("f",data[44:48])[0]
               self.throttle=struct.unpack("f",data[48:52])[0]
               self.brake=struct.unpack("f",data[52:56])[0]
               self.clutch=struct.unpack("f",data[56:60])[0]
               self.display1=data[60:76]
               self.display2=data[76:92]
               #outgauge_pack = struct.unpack('I3sxH2B7f2I3f15sx15sxI', data)
               #print "ID :", struct.unpack("i",data[92:96])

def getx(radius,angle):
    return radius*math.cos(angle* math.pi / 180.0)
def gety( radius, angle):
    return radius*math.sin(angle* math.pi / 180.0)
    
class Renderer(Thread):
     def __init__(self):
          Thread.__init__(self)
          GLCD_SDK.initDLL("LogitechLcdEnginesWrapper.dll")
          GLCD_SDK.LogiLcdInit("OutGauge.py", GLCD_SDK.TYPE_COLOR + GLCD_SDK.TYPE_MONO);
          if GLCD_SDK.LogiLcdIsConnected(GLCD_SDK.TYPE_COLOR) or GLCD_SDK.LogiLcdIsConnected(GLCD_SDK.TYPE_MONO):
               self.work = True
               self.im = Image.new("RGBA", (320, 240), "Black")
               self.im2 = Image.new("RGBA", (320, 240), "Black")
               self.usr_font = ImageFont.truetype("C:\Windows\Fonts\EHSMB.TTF", 20)
               self.usr_font_big = ImageFont.truetype("C:\Windows\Fonts\EHSMB.TTF", 40)
               draw = ImageDraw.Draw(self.im)
               draw.ellipse((10,10,310,310), outline="White", fill="Black")
               i=0
               draw.ellipse((60,60,260,260), outline="White", fill="Black")
               while i<25:
                    if(i==5 or i==9 or i==13):
                        color = "Blue"
                    else:
                        color = "White"
                    if( i%2 == 0 ):
                        cercleext = 144
                    else:
                        cercleext = 135
                    angle = 150+i*10
                    draw.line( (getx(150, angle)+160, gety(150, angle)+160,getx(cercleext, angle)+160, gety(cercleext, angle)+160) , fill=color)
                    i+=1
                    
               i=0
               while(i<33):
                    if(i%4==0):
                         cercleext = 90;
                         width = 2
                    else:
                         cercleext = 95;
                         width = 1
                    if(28<=i):
                         color="Blue"
                    else:
                         color="White"
                    angle = 150+i*7.5
                    draw.line( (getx(100, angle)+160, gety(100, angle)+160,getx(cercleext, angle)+160, gety(cercleext, angle)+160) , fill=color, width=width)
                    i+=1
               
               draw.rectangle( (130,120,190,140), fill="#007FFF")
               draw.rectangle( (130,170,190,235), fill="#007FFF")
               
               self.draw2 = ImageDraw.Draw(self.im2)
          else:
               self.work = False
     
     def run(self):
          while self.work:
               self.im2.paste(self.im)
               #self.draw2.bitmap((0,0), self.im)
               self.draw2.text((135,120), "%4.0f"%udpthread.RPM , font=self.usr_font, fill="#000")
               self.draw2.text((140,170), "%3.0f"%(udpthread.speed*3.6) , font=self.usr_font, fill="#000")
               
               if(udpthread.gear >250):
                    self.draw2.text((140,200), "R2" , font=self.usr_font_big, fill="#000")
               elif(udpthread.gear == 0):
                    self.draw2.text((140,200), "R" , font=self.usr_font_big, fill="#000")
               elif(udpthread.gear == 1):
                    self.draw2.text((140,200), "N" , font=self.usr_font_big, fill="#000")
               else:
                    self.draw2.text((140,200), "%d"%(udpthread.gear-1) , font=self.usr_font_big, fill="#000")
               
               
               angle = udpthread.speed*3.6 + 150
               self.draw2.line((getx(100,angle)+160, gety(100,angle)+160, getx(140,angle)+160,gety(140,angle)+160), fill=(0,0,255,255))
               angle= udpthread.RPM/33.3333 + 150;
               self.draw2.line((getx(90,angle)+160, gety(90,angle)+160, getx(0,angle)+160,gety(0,angle)+160), fill=(0,0,255,255))
               
               GLCD_SDK.ColorBGPIL(self.im2)
               #GLCD_SDK.LogiLcdColorSetText(7,str(udpthread.speed*3.6),127,127,127)
               GLCD_SDK.LogiLcdUpdate()
          


if __name__ == "__main__":
     ctypes.windll.kernel32.SetConsoleTitleA("G_outgauge.py")
     global udpthread
     udpthread = OutgaugeServer('127.0.0.1')
     udpthread.start()
     render = Renderer()
     render.start()
     
     udpthread.join()
