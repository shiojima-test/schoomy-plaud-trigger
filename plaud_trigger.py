import serial
import subprocess
import time

is_recording = False

CLICLICK = "/opt/homebrew/bin/cliclick"

def start_plaud_recording():
    subprocess.run(["open", "plaud://record"])
    time.sleep(2)
    subprocess.run([CLICLICK, "c:1319,111"])

def stop_plaud_recording():
    subprocess.run([CLICLICK, "c:1593,357"])

def connect():
    while True:
        try:
            ser = serial.Serial()
            ser.port = '/dev/cu.SLAB_USBtoUART'
            ser.baudrate = 9600
            ser.timeout = 1
            ser.open()
            print("スクーミー接続しました")
            return ser
        except Exception as e:
            print(f"接続待機中... ({e})")
            time.sleep(3)

print("スクーミー待機中...")
ser = connect()

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line == "RECORD_START":
            if not is_recording:
                print("録音開始！")
                start_plaud_recording()
                is_recording = True
            else:
                print("録音停止！")
                stop_plaud_recording()
                is_recording = False
    except Exception as e:
        print(f"切断されました。再接続します... ({e})")
        is_recording = False
        time.sleep(3)
        ser = connect()
