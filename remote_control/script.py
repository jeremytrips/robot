import serial

ser = serial.Serial("/dev/ttyACM0", 9600)
run = True

while run:
    a = input(">")
    if a == "z":
        ser.write("1%".encode('utf-8'))

    if a=="q":
        ser.write("2%".encode('utf-8'))
        
    if a == "d":
        ser.write("3%".encode('utf-8'))

    if a == "s":
        ser.write("4%".encode('utf-8'))

    if a == "":
        ser.write("0%".encode('utf-8'))

    if a == "p":
        run = False