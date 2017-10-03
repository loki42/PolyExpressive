import struct
import machine
i2c = machine.I2C(scl=machine.Pin(33), sda=machine.Pin(32), freq=100000)

def writeRegister8(r, v):
    i2c.writeto_mem(65, r, bytes([v]))

STMPE_ADDR=0x41

STMPE_SYS_CTRL1=0x03
STMPE_SYS_CTRL1_RESET=0x02
STMPE_SYS_CTRL2=0x04
STMPE_TSC_CTRL=0x40
STMPE_TSC_CTRL_EN=0x01
STMPE_TSC_CTRL_XYZ=0x00
STMPE_TSC_CTRL_XY=0x02
STMPE_INT_CTRL=0x09
STMPE_INT_CTRL_POL_HIGH=0x04
STMPE_INT_CTRL_POL_LOW=0x00
STMPE_INT_CTRL_EDGE=0x02
STMPE_INT_CTRL_LEVEL=0x00
STMPE_INT_CTRL_ENABLE=0x01
STMPE_INT_CTRL_DISABLE=0x00

STMPE_INT_EN=0x0A
STMPE_INT_EN_TOUCHDET=0x01
STMPE_INT_EN_FIFOTH=0x02
STMPE_INT_EN_FIFOOF=0x04
STMPE_INT_EN_FIFOFULL=0x08
STMPE_INT_EN_FIFOEMPTY=0x10
STMPE_INT_EN_ADC=0x40
STMPE_INT_EN_GPIO=0x80

STMPE_INT_STA=0x0B
STMPE_INT_STA_TOUCHDET=0x01

STMPE_ADC_CTRL1=0x20
STMPE_ADC_CTRL1_12BIT=0x08
STMPE_ADC_CTRL1_10BIT=0x00

STMPE_ADC_CTRL2=0x21
STMPE_ADC_CTRL2_1_625MHZ=0x00
STMPE_ADC_CTRL2_3_25MHZ=0x01
STMPE_ADC_CTRL2_6_5MHZ=0x02

STMPE_TSC_CFG=0x41
STMPE_TSC_CFG_1SAMPLE=0x00
STMPE_TSC_CFG_2SAMPLE=0x40
STMPE_TSC_CFG_4SAMPLE=0x80
STMPE_TSC_CFG_8SAMPLE=0xC0
STMPE_TSC_CFG_DELAY_10US=0x00
STMPE_TSC_CFG_DELAY_50US=0x08
STMPE_TSC_CFG_DELAY_100US=0x10
STMPE_TSC_CFG_DELAY_500US=0x18
STMPE_TSC_CFG_DELAY_1MS=0x20
STMPE_TSC_CFG_DELAY_5MS=0x28
STMPE_TSC_CFG_DELAY_10MS=0x30
STMPE_TSC_CFG_DELAY_50MS=0x38
STMPE_TSC_CFG_SETTLE_10US=0x00
STMPE_TSC_CFG_SETTLE_100US=0x01
STMPE_TSC_CFG_SETTLE_500US=0x02
STMPE_TSC_CFG_SETTLE_1MS=0x03
STMPE_TSC_CFG_SETTLE_5MS=0x04
STMPE_TSC_CFG_SETTLE_10MS=0x05
STMPE_TSC_CFG_SETTLE_50MS=0x06
STMPE_TSC_CFG_SETTLE_100MS=0x07

STMPE_FIFO_TH=0x4A

STMPE_FIFO_SIZE=0x4C

STMPE_FIFO_STA=0x4B
STMPE_FIFO_STA_RESET=0x01
STMPE_FIFO_STA_OFLOW=0x80
STMPE_FIFO_STA_FULL=0x40
STMPE_FIFO_STA_EMPTY=0x20
STMPE_FIFO_STA_THTRIG=0x10

STMPE_TSC_I_DRIVE=0x58
STMPE_TSC_I_DRIVE_20MA=0x00
STMPE_TSC_I_DRIVE_50MA=0x01

STMPE_TSC_DATA_X=0x4D
STMPE_TSC_DATA_Y=0x4F
STMPE_TSC_FRACTION_Z=0x56

STMPE_GPIO_SET_PIN=0x10
STMPE_GPIO_CLR_PIN=0x11
STMPE_GPIO_DIR=0x13
STMPE_GPIO_ALT_FUNCT=0x17

def init_st():

    writeRegister8(STMPE_SYS_CTRL1, STMPE_SYS_CTRL1_RESET)
    for i in range(65):
        i2c.readfrom_mem(65, i, 1)

    writeRegister8(STMPE_SYS_CTRL2, 0x0) # turn on clocks!
    writeRegister8(STMPE_TSC_CTRL, STMPE_TSC_CTRL_XYZ | STMPE_TSC_CTRL_EN) # XYZ and enable!
    # writeRegister8(STMPE_INT_EN, STMPE_INT_EN_TOUCHDET)
    writeRegister8(STMPE_INT_EN, 0)
    writeRegister8(STMPE_ADC_CTRL1, STMPE_ADC_CTRL1_12BIT | (0x6 << 4)) # 96 clocks per conversion
    writeRegister8(STMPE_ADC_CTRL2, STMPE_ADC_CTRL2_3_25MHZ)
    writeRegister8(STMPE_TSC_CFG, STMPE_TSC_CFG_4SAMPLE | STMPE_TSC_CFG_DELAY_1MS | STMPE_TSC_CFG_SETTLE_5MS)
    writeRegister8(STMPE_TSC_FRACTION_Z, 0x7)
    writeRegister8(STMPE_FIFO_TH, 1)
    writeRegister8(STMPE_FIFO_STA, STMPE_FIFO_STA_RESET)
    writeRegister8(STMPE_FIFO_STA, 0)    # unreset
    writeRegister8(STMPE_TSC_I_DRIVE, STMPE_TSC_I_DRIVE_20MA)
    writeRegister8(STMPE_INT_STA, 0xFF) # reset all ints
    writeRegister8(STMPE_INT_CTRL, STMPE_INT_CTRL_POL_HIGH | STMPE_INT_CTRL_ENABLE)


def get_p():
    status = False
    if (int.from_bytes(i2c.readfrom_mem(65, STMPE_FIFO_STA, 1), 'big') & STMPE_FIFO_STA_EMPTY):
        return (status, 0, 0, 0)
    else:
        x = 0
        y = 0
        x = 0
        while not (int.from_bytes(i2c.readfrom_mem(65, STMPE_FIFO_STA, 1), 'big') & STMPE_FIFO_STA_EMPTY):
            # if buffer not empty
            x = struct.unpack('>H', i2c.readfrom_mem(65, 0x4D, 2))[0]
            y = struct.unpack('>H', i2c.readfrom_mem(65, 0x4F, 2))[0]
            z = struct.unpack('>B', i2c.readfrom_mem(65, 0x51, 1))[0]
            status = True
        # reset interrupt
        writeRegister8(STMPE_INT_STA, 0xFF)#  reset all ints
        return (status, x, y, z)

def get_point():
    # return x, y, z by processing z1 and z2
    # convert to mm
    panel_x = 469 # active area of panel
    panel_y = 294
    status, in_x, in_y, in_z = get_p()
    if status:
        x = panel_x * ((4095 - in_x) / 4095)
        y = panel_y * ((4095 - in_y) / 4095)
        z = 0
        if in_z > 5:
            z = 256 - in_z
        return (status, x, y, z)
    else:
        return (False, 0, 0, 0)

# init
init_st()

