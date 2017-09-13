from machine import I2C
import struct

i2c = I2C(0, I2C.MASTER)
# i2c.readfrom_mem(72, 0b0001, 2)
# cfr0_addr = 0xD
# cr0 = 0b10101000
# cr0_2 = 0b00000000



# general startup? 
cb0 = 0b11100010
cb0_h = b'\xe2'
# set to 12 bit, xyz reset registers
cb1 = 0b10000110
cb1_h = b'\x86'



# i2c.writeto_mem(address, res_reg, b'\x00')
i2c.writeto(72, bytes([0x84])) # no reset

i2c.writeto(72, cb1_h)
# ts = bytes([0xE2, cr0, cr0_2])
# i2c.writeto(72, ts)

# i2c.writeto(72, cb1_h)

# cr0_psm = 0b01100010 # send to start conversion byt setting PSM mode
# psm_1 = 0b10101000
# psm_2 = 0b00000000
# ts = bytes([cr0_psm, psm_1, psm_2])
# i2c.writeto(72, ts)

# settling time
cr0_psm = 0b01100010 # send to start conversion byt setting PSM mode
psm_1 = 0b10101011 # 1 ms settling time
psm_2 = 0b00000000
ts = bytes([cr0_psm, psm_1, psm_2])
i2c.writeto(72, ts)

# set to 12 bit, xyz no reset
cb1_noreset = 0b10000100
i2c.writeto(72, bytes([cb1_noreset]))


def get_p():
    # x
    rb = 0b00000011
    rb_x =b'\x03'
    i2c.writeto(72, rb_x)

    x = struct.unpack('>H', i2c.readfrom(72, 2))[0]

    # y
    rb = 0b00001011
    rb_y =b'\x0b'
    i2c.writeto(72, rb_y)

    y = struct.unpack('>H', i2c.readfrom(72, 2))[0]

    # z1
    rb = 0b00010011
    rb_y =b'\x13'
    i2c.writeto(72, rb_y)

    z1 = struct.unpack('>H', i2c.readfrom(72, 2))[0]

    # z2
    rb = 0b00011011
    rb_y =b'\x1b'
    i2c.writeto(72, rb_y)

    z2 = struct.unpack('>H', i2c.readfrom(72, 2))[0]
    return (x, y, z1, z2)

def get_point():
    # return x, y, z by processing z1 and z2
    # convert to mm
    panel_x = 469 # active area of panel
    panel_y = 294
    in_x, in_y, in_z1, in_z2 = get_p()
    x = panel_x * ((4095 - in_x) / 4095)
    y = panel_y * ((4095 - in_y) / 4095)
    z = 0
    if in_z2 > 5:
        z = 4095 - in_z2
    return (x, y, z)
