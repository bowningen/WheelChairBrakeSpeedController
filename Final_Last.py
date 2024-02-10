import serial
import time
import os
import logging
import configparser
import multiprocessing
from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager

pwd = os.getcwd()

logging.basicConfig(
    level=logging.DEBUG, format="%(processName)s_%(threadName)s: %(message)s"
)


config = configparser.ConfigParser()
config.read("config.ini", encoding = "UTF-8")


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
ser.port = "COM2"     #デバイスマネージャでArduinoのポート確認
ser.baudrate = 9600 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止
#if not ser.isOpen():
    #ser.open()
#print('com2 is open', ser.isOpen())
#CHIBIKKO(motor)
serM = serial.Serial()
serM.port = "COM1"     #デバイスマネージャでArduinoのポート確認
serM.baudrate = 9600 #Arduinoと合わせる
serM.setDTR(False)     #DTRを常にLOWにしReset阻止
#serM.open()            #COMポートを開く 

def process1(P_BOX,P_FLAG,E_Check,R_BOX):

    #ここのpath変えるのわすれない
    logging.debug(f"start (pid:{os.getpid()})")

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
            time2 = ser.readline() #改行があるまで読み取り
            #print(time2)
            time3 = time2.decode('UTF-8')
            time2 = time3.replace('\'', '').replace('b','').replace('\r','').replace('\n','')
            if (len(time2) >  5):
                break
            else:
                continue
        
        if (time2 == "" or time2 == "\n" or time2 == "\r\n" or time2 == "\r"):
            time2 = time1
        time2 = float(str(time2).strip()) #空白・改行を除く、文字列にする、→floatに
        time2 = time2 * 0.001 #秒に変換


        for k in range(2):
            #ser.write(b' ') #データ送信
            #time.sleep(1)
            #果たしてこのsleep、1sもいるのか...？
            data = ser.readline() #改行があるまで読み取り
            data2 = data.decode()
            data = data2.replace('\'', '').replace('b','').replace('\r','').replace('\n','')
            if (data == "" or data == "\n" or data == "\r\n" or time2 == "\r"):
                data = 2.4
            data = float(str(data).strip()) #空白・改行を除く、文字列にする、→floatに

            #print(data)

            if abs(data - VTE_OFF) > VTE_ERROR: #磁石近づいてるとき...
                dtime = time2 - time1 #前に磁石近づいたときとの時間の変化量(シリアル通信で送ってもらいたい)
                if dtime > 0.01: #前近づいたときから何秒か空いてたら(適当)
                    #計算上ふつうは0.3s間隔ぐらいで近づくはず
                    time1 = time2
                    speed = DIST / dtime
                    #print(speed)
                    if (k == 0):
                        L_speed = speed
                    else:
                        R_speed = speed
            
            if (time2 - time1 > 2):
                L_speed = 0
                R_speed = 0

        
        #print("sp" + str(L_speed))
        #print("sp" + str(R_speed))
        L_POS, R_POS = motor(L_speed,R_speed,time2) #まわす
        #f.write("Time  :  " + str(T) + "\n\n")
        #f.write("Speed :  " + "L : " + str(L) + "  R : " + str(R) + "\n")
        #f.write("Break :  " + "L : " + str(L_POS) + "  R : " + str(R_POS))
        #f.write("")

        #格納
        if (etc < 65530):
            etc2 = etc + 1
            etc3 = etc + 2
            etc4 = etc + 3
            etc5 = etc + 4
            R_BOX[etc] = float(time2)
            R_BOX[etc2] = float(L_speed)
            R_BOX[etc3] = float(R_speed)
            R_BOX[etc4] = int(L_POS)
            R_BOX[etc5] = int(R_POS)
            etc = etc + 5

        #dainyuu
        P_BOX[sfck] = L_POS
        sfck += 1
        P_BOX[sfck] = R_POS
        sfck += 1
        while True:
            tp = round(time.time,1)
            if(tp % 2 == 0):
                break
            else:
                continue

        #print(sfck)
        #SHIFT
        if (P_FLAG[0] == True):
            pbr = 0
            #range(253)かも...(元々0~255だがこれって...)
            for i in range(254):
                pbrN = pbr + 2
                P_BOX[pbr] = P_BOX[pbrN]
                pbr += 1
            sfck = sfck - 2
            P_FLAG[0] = False
        elif (sfck == 253 or sfck == 254):
            #P_FLAG[0] = True
            pbr = 0
            #range(253)かも...(元々0~255だがこれって...)
            for i in range(254):
                pbrN = pbr + 2
                P_BOX[pbr] = P_BOX[pbrN]
                pbr += 1
            sfck = sfck - 2


    ser.close()
    
#for motor moving
def process2(P_BOX,P_FLAG,LP,RP,L_last,R_last,MotorIO,E_Check):
    logging.debug(f"start (pid:{os.getpid()})")
    while True:
        if (P_FLAG[0] == False):
            LP[0] = P_BOX[0]
            RP[0] = P_BOX[1]
            if (LP[0] != L_last[0] or RP[0] != R_last[0]):
                while True:
                    #print(MotorIO[0])
                    while True:
                        tp = round(time.time,1)
                        if(tp % 2 == 1):
                            break
                        else:
                            continue
                    #if (MotorIO[0] == False):
                    print("3")
                    test = bytes((str(len(str(LP[0]))) + str(LP[0]).zfill(3)+ str(len(str(RP[0]))) + str(RP[0]).zfill(3)).encode("UTF-8"))
                    serM.write(test)
                    L_last[0] = LP[0]
                    R_last[0] = RP[0]
                    MotorIO[0] = True
                    P_FLAG[0] = True
                    break
                    #else:
                        #continue 

#for cheking motor      
#と、あと各Listのリセット           
def process3(P_BOX,P_FLAG,LP,RP,L_last,R_last,MotorIO,E_Check):
    logging.debug(f"start (pid:{os.getpid()})")
    #P_BOX(Motor Power)格納List、 Range:256
    pre = 0
    for i in P_BOX:
        P_BOX[pre] = 0
        pre += 1
    #P_BOXの中シフト実行中かどうかの確認
    P_FLAG[0] = True
    #Left Motor Power
    LP[0] = 98
    #Right Motor Power
    RP[0] = 65
    #Resent(?) Left Motor Power
    L_last[0] = 0
    #Resent(?) Right Motor Power
    R_last[0] = 0
    #Motorくんうごいてるかな？
    MotorIO[0] = False

    while True:
        ioc = serM.readline() #改行があるまで読み取り
        MotorIO[0] = False

def motor(L, R, T):
    speedBox = [L,R]#格納

    POS_MINL = int(config["SETTINGS"]["POS_MINL"]) #ブレーキの効く最小角
    POS_MAXL = int(config["SETTINGS"]["POS_MAXL"]) #一応最大の回転角
    POS_MINR = int(config["SETTINGS"]["POS_MINR"]) #ブレーキの効く最小角
    POS_MAXR = int(config["SETTINGS"]["POS_MAXR"]) #一応最大の回転角
    minSP = int(config["SETTINGS"]["minSP"]) #ブレーキかけ始める最小速度
    maxSP = int(config["SETTINGS"]["maxSP"]) #限界までブレーキをかけるときの速度
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
    #set_angle(float(RD),SERV1)
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

    #set_angle(float(RD),SERV2)
    R_POS = int(RD) #現在位置
               
    #test = bytes((str(len(str(L_POS))) + str(L_POS).zfill(3)+ str(len(str(R_POS))) + str(R_POS).zfill(3)).encode("UTF-8"))
    #ser.write(test)
    #print(str(test))
    #LP = L_POS
    #RP = R_POS
        
    #書き込み(量がとんでもないのでいったん配列に格納)
    #with open(resultPath, mode = "w") as f:
        #f.write("Time  :  " + str(T) + "\n\n")
        #f.write("Speed :  " + "L : " + str(L) + "  R : " + str(R) + "\n")
        #f.write("Break :  " + "L : " + str(L_POS) + "  R : " + str(R_POS))
        #f.write("")

    return L_POS,R_POS
            
#def process4(E_Check):
    #E_Check[0] = 0
    #while True:
        #pwd = input()
        #if (pwd == "@"):
            #E_Check[0] = 10
            #break
        #else:
            #continue

def main():
    global RR
    with SharedMemoryManager() as smm:
        P_BOX = smm.ShareableList(range(256))
        P_FLAG = smm.ShareableList(range(1))
        LP = smm.ShareableList(range(1))
        RP = smm.ShareableList(range(1))
        L_last = smm.ShareableList(range(1))
        R_last = smm.ShareableList(range(1))
        MotorIO = smm.ShareableList(range(1))
        E_Check = smm.ShareableList(range(1))
        R_BOX = smm.ShareableList(range(65535))
        logging.debug(f"start (pid:{os.getpid()})")
        #p4 = Process(target=process4, args=(E_Check))
        p3 = Process(target=process3, args=(P_BOX,P_FLAG,LP,RP,L_last,R_last,MotorIO,E_Check,))
        p2 = Process(target=process2, args=(P_BOX,P_FLAG,LP,RP,L_last,R_last,MotorIO,E_Check,))
        p1 = Process(target=process1, args=(P_BOX,P_FLAG,E_Check,R_BOX,))

        # プロセスの開始
        p1.start()
        p2.start()
        p3.start()

        # プロセスの終了を待機
        p1.join()
        p2.join()   
        p3.join() 
        RR = R_BOX


if __name__ == '__main__':
    main()

    #with open(resultPath, mode = "w") as f:
        #f.write("Time  :  " + str(T) + "\n\n")
        #f.write("Speed :  " + "L : " + str(L) + "  R : " + str(R) + "\n")
        #f.write("Break :  " + "L : " + str(L_POS) + "  R : " + str(R_POS))
        #f.write("")
with open(resultPath, mode = "w") as f:
    ty = 0
    for et in RR:
        ty2 = ty + 1
        ty3 = ty + 2
        ty4 = ty + 3
        ty5 = ty + 4
        f.write(f"Time : {str(RR[ty])}\n")
        f.write(f"Speed : L = {str(RR[ty2])} , R = {str(RR[ty3])}\n")
        f.write(f"Break : L = {str(RR[ty4])} , R = {str(RR[ty5])}\n")
        ty = ty + 5
