python3 -c "
import serial, time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)
print('Reading TOF and distance...')
print(f'{'TOF (µs)':>12} {'DIST (cm)':>12}')
print('-' * 26)
while True:
    line = ser.readline().decode().strip()
    if ',' in line and 'TOF:' in line:
        parts = line.split(',')
        tof  = float(parts[0].replace('TOF:', ''))
        dist = float(parts[1].replace('DIST:', ''))
        if tof > 0:
            print(f'{tof:>12.1f} {dist:>12.1f}')
"
