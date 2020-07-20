import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial

# Принимает пакет вида [0xAA 0xAA {2 байта x координат} {2 байта y координат 1 функции} {2 байта y координат 2 функции} {2 байта y координат 3 функции}]
# {2 байта координат} идут в  численном виде целого числа (для передачи float необходимо заранее домножить на 10^n перед отправкой, а ТУТ разделить на это же число), где младший байт приходит первее
# По отмеченным коментариям можно настроить параметры передачи и отображения графиков
# Запускать скрипт до начала передачи

def init():
    # Установить необходимые границы x y координаты каждого графика
    ax[0].set_ylim(0, 3.3)
    ax[0].set_xlim(0, 10)

    ax[1].set_ylim(0, 3.3)
    ax[1].set_xlim(0, 10)
    
    ax[2].set_ylim(0, 3.3)
    ax[2].set_xlim(0, 10)
    
    del xdata[:]
    del ymain[:]
    del yintegral[:]
    del ydiff[:]

    line_main.set_data(xdata, ymain)
    line_integral.set_data(xdata, yintegral)
    line_diff.set_data(xdata, ydiff)
    return [line_main, line_integral, line_diff]


def run(data):
    title = b'\xAA\xAA'
    rx = ser.read(size=2)
    while rx!=title:
        rx = ser.read(size=2)
    rx = ser.read(size=4)
    # Настроить деление для передачи вещественных чисел (1000 - оптимально)
    x = int.from_bytes(rx[0:2], 'little')/1000
    y1 = int.from_bytes(rx[2:4], 'little')/1000
    y2 = int.from_bytes(rx[4:6], 'little')/1000
    y3 = int.from_bytes(rx[6:8], 'little')/1000
    
    xdata.append(x)
    ymain.append(y1)
    yintegral.append(y2)
    ydiff.append(y3)

    line_main.set_data(xdata, ymain)
    line_integral.set_data(xdata, yintegral)
    line_diff.set_data(xdata, ydiff)
    return [line_main, line_integral, line_diff]


# Можно изменить figsize, если не вмещается окошко. lw - толщина линии 
fig, ax = plt.subplots(3, 1, figsize=(7, 10))
line_main,      = ax[0].plot([],[], 'b', lw=1.5)
line_integral,  = ax[1].plot([],[], 'r', lw=1.5)
line_diff,      = ax[2].plot([],[], 'g', lw=1.5)

ax[0].grid()
ax[1].grid()
ax[2].grid()
# Название графиков
ax[0].set_title('Main function')
ax[1].set_title('Integration')
ax[2].set_title('Differentiation')

xdata, ymain, yintegral, ydiff = [], [], [], []

# Установить номер COM-порта и скорость
ser = serial.Serial('COM3', 115200)
# interval - период опроса COM порта в миллисекундах
ani = FuncAnimation(fig, run, interval=10, init_func=init)
plt.show()