import serial
import time
import os
import logging
import configparser

pwd = os.getcwd()



config = configparser.ConfigParser()
config.read("config.ini", encoding = "SHIFT-JIS")


resultPath = str(config["SETTINGS"]["RESULT"])

HOLE1 = int(config["SETTINGS"]["HOLE1"])
HOLE2 = int(config["SETTINGS"]["HOLE2"])
SERV1 = str(config["SETTINGS"]["SERV1"])
SERV2 = str(config["SETTINGS"]["SERV2"])
gp_outL = int(config["SETTINGS"]["gp_outL"])
gp_outR = int(config["SETTINGS"]["gp_outR"])

RR = []

#UNO(sensor)
ser = serial.Serial()
ser.port = str(config["SETTINGS"]["ARDUINO1"])   #デバイスマネージャでArduinoのポート確認
ser.baudrate = 115200 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止
ser.open()

serM = serial.Serial()
serM.port = str(config["SETTINGS"]["ARDUINO2"])     #デバイスマネージャでArduinoのポート確認
serM.baudrate = 115200 #Arduinoと合わせる
serM.setDTR(False)     #DTRを常にLOWにしReset阻止
serM.open()            #COMポートを開く 

MotorIO = False
P_BOX = []
LP = 0
RP = 0
L_last = 0
R_last = 0
Lt = 0
def main():
    global MotorIO
    global P_BOX
    global LP
    global RP
    global L_last
    global R_last
    global Lt
    test = bytes((str(len(str(77))) + str(90).zfill(3)+ str(len(str(77))) + str(95).zfill(3)).encode("utf-8"))
    serM.write(test)


    time1 = 0
    TIRE = int(config["SETTINGS"]["TIRE"]) #タイヤ何インチか(1inch = 0.0254m)
    MAG_NUM = int(config["SETTINGS"]["MAG_NUM"]) #磁石の個数
    DIST = TIRE * 0.0254 * 3.14 / MAG_NUM #一回磁石が近づくときの移動距離
    VTE_OFF = float(config["SETTINGS"]["VTE_OFF"]) #何もないときの電圧
    VTE_ERROR = float(config["SETTINGS"]["VTE_ERROR"]) #許容する誤差(V)
    
    L_speed = 0
    R_speed = 0
    
    etc = 0
    sfck = 0
    while True:
        #ser.write(b' ') #データ送信
        while True:
            time2 = ser.readline() #改行があるまで読み取る
            time2 = float(repr(time2.decode())[1:-5])
            	
            if (len(str(time2)) >  7 or str(time2).count(".") == 1):
                break
            else:
                continue
        
        if (time2 == "" or time2 == "\n" or time2 == "\r\n" or time2 == "\r"):
            time2 = time1
        time2 = float(str(time2).strip()) #空白・改行を除く、文字列にする、→floatに
        time2 = time2 * 0.001 #秒に変換


        for k in range(2):
            data = ser.readline() #改行があるまで読み取り
            data = float(repr(data.decode())[1:-5])
            if (data == "" or data == "\n" or data == "\r\n" or time2 == "\r"):
                data = 2.4
            data = float(str(data).strip()) #空白・改行を除く、文字列にする、→floatに

            if abs(data - VTE_OFF) > VTE_ERROR: #磁石近づいてるとき...
                dtime = time2 - time1 #前に磁石近づいたときとの時間の変化量(シリアル通信で送ってもらいたい)
                if dtime > 0.1: #前近づいたときから何秒か空いてたら(適当)
                    #計算上ふつうは0.3s間隔ぐらいで近づくはず
                    time1 = time2
                    speed = DIST / dtime
                    
                    if (speed < 3.2 and speed > 3.0):
                        speed = 0
                    print(speed)
                    if (k == 0):
                        L_speed = speed
                    else:
                        R_speed = speed
            
            if (time2 - time1 > 2):
                L_speed = 0
                R_speed = 0

        
        L_POS, R_POS = motor(L_speed,L_speed,time2) #まわす
        if (time2 > Lt + 1):
            test = bytes((str(len(str(L_POS))) + str(L_POS).zfill(3)+ str(len(str(R_POS))) + str(R_POS).zfill(3)).encode("utf-8"))
            serM.write(test)
            print(test)
            Lt = time2
    ser.close()
    
def motor(L, R, T):
    speedBox = [float(L),float(R)]#格納

    POS_MINL = int(config["SETTINGS"]["POS_MINL"]) #ブレーキの効く最小角
    POS_MAXL = int(config["SETTINGS"]["POS_MAXL"]) #一応最大の回転角
    POS_MINR = int(config["SETTINGS"]["POS_MINR"]) #ブレーキの効く最小角
    POS_MAXR = int(config["SETTINGS"]["POS_MAXR"]) #一応最大の回転角
    minSP = float(config["SETTINGS"]["minSP"]) #ブレーキかけ始める最小速度
    maxSP = float(config["SETTINGS"]["maxSP"]) #限界までブレーキをかけるときの速度
    LM = 0 #モーターON/OFF検知(重複して動作させないためだがいらない気が...)
    RM = 0 #なんでつくったんだっけ...？
    pp = 0 #左右どっちかな

    R_POS = 0.0
    L_POS = 0.0

    if (minSP < L and L < maxSP): #速度がブレーキ調整可能範囲の場合
        SPU = L - minSP
        REN = maxSP - minSP
        WA = SPU / REN
        RD = POS_MINL + ((POS_MAXL - POS_MINL) * WA)
    elif (L > maxSP): #速度がブレーキ調整可能範囲を上回っている場合
        RD = POS_MAXL
    else: # まだブレーキかけないよ
        RD = POS_MINL
        
    #うごきます
    L_POS = int(RD) #現在位置
        
    if (minSP < R and R < maxSP): #速度がブレーキ調整可能範囲の場合
        SPU = R - minSP
        REN = maxSP - minSP
        WA = SPU / REN
        RD = POS_MAXR + ((POS_MINR - POS_MAXR) * WA)
    elif (R > maxSP): #速度がブレーキ調整可能範囲を上回っている場合
        RD = POS_MAXR
    else: # まだブレーキかけないよ
        RD = POS_MINR

    R_POS = int(RD) #現在位置
               
    return L_POS,R_POS

if __name__ == '__main__':
    main()
