import serial
import time
from datetime import datetime
import mpytool
# Set your serial port and baudrate here
SERIAL_PORT = '/dev/ttyACM0'  # e.g. '/dev/ttyUSB0' on Linux/Mac or 'COM3' on Windows
BAUDRATE = 115200

# Set your target time (or use current time)
#now = datetime.now()
#year, month, day = now.year, now.month, now.day
#hour, minute, second = now.hour, now.minute, now.second

# Create the datetime command string for MicroPython
#datetime_command = f"ds.datetime(({year}, {month}, {day}, {hour}, {minute}, {second}))\r\n"




def main():
    conn = mpytool.ConnSerial(port=SERIAL_PORT, baudrate=BAUDRATE)
    mpy = mpytool.Mpy(conn)
    #mpy.comm.exec("test_board()")
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    hour, minute, second = now.hour, now.minute, now.second
    
    # Create the datetime command string for MicroPython
    print("Setting time..")
    datetime_command = f"ds.datetime(({year}, {month}, {day}, {hour}, {minute}, {second}))\r\n"
    response = mpy.comm.exec_eval(datetime_command)
    print(response)
    print("Checking time..")
    response = mpy.comm.exec("print(get_timestamp())") 
    print(str(response))
    print("checking volts..")
    response = mpy.comm.exec("print(get_batt_v())") 
    print(str(response))
    print("deleting log..")
    response = mpy.comm.exec("delete_log()") 
    print(str(response))
    print("Resetting board..")
    mpy.soft_reset()
    
#    try:
#        with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as ser:
#            time.sleep(2)  # Wait for the connection to stabilize
#            
##            print("Resetting device with Ctrl+D...")
##            ser.write(b'\x04')  # Ctrl+D (soft reset)
##            time.sleep(1)
#
#            print("Interrupting with Ctrl+C...")
#            ser.write(b'\x03')  # Ctrl+C (interrupt)
#            time.sleep(1)
#            ser.write("\r\n".encode())  #errout
#            time.sleep(1)
#            # Optional: read response
#            response = ser.read_all().decode(errors='ignore')
#            print("Response from device:")
#            print(response)
#
#            print("Sending datetime set command...")
#            # Set your target time (or use current time)
#            now = datetime.now()
#            year, month, day = now.year, now.month, now.day
#            hour, minute, second = now.hour, now.minute, now.second
#            
#            # Create the datetime command string for MicroPython
#            datetime_command = f"ds.datetime(({year}, {month}, {day}, {hour}, {minute}, {second}))\r\n"
#            print(datetime_command)
#            ser.write(datetime_command.encode())
#            time.sleep(1)
#
#
#
#
#            # Optional: read response
#            response = ser.read_all().decode(errors='ignore')
#            print("Response from device:")
#            print(response)
#            
#
#            ser.write("delete_log()\r\n".encode())
#            time.sleep(0.5)
#            #ser.write("go_to_sleep()\r\n".encode())
#            #ser.write("\r\n".encode())
#            #time.sleep(0.1)
#
#            response = ser.read_all().decode(errors='ignore')
#            print("Response from device:")
#            print(response)
#
#
#
#    except serial.SerialException as e:
#        print(f"Serial error: {e}")

if __name__ == '__main__':
    main()

