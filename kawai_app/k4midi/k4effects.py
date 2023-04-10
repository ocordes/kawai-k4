# k4effects.py
#
# written by: Oliver Cordes 2023-04-10
# changed by: Oliver Cordes 2023-04-10

from k4midi.k4base import K4Base

class K4Effects(K4Base):
    id = 0x14
    size = 35

    effect_type = property(*K4Base.func_template(00, mask=0b1111, correct=1))
    para1 = property(*K4Base.func_template(1, mask=0b111))
    para2 = property(*K4Base.func_template(2, mask=0b111))
    para3 = property(*K4Base.func_template(3, mask=0b11111))

    pan_A = property(*K4Base.func_template(10, mask=0b11111, correct=-8))
    send1_A = property(*K4Base.func_template(11, mask=0b1111111))
    send2_A = property(*K4Base.func_template(12, mask=0b1111111))

    pan_B = property(*K4Base.func_template(13, mask=0b11111, correct=-8))
    send1_B = property(*K4Base.func_template(14, mask=0b1111111))
    send2_B = property(*K4Base.func_template(15, mask=0b1111111))

    pan_C = property(*K4Base.func_template(16, mask=0b11111, correct=-8))
    send1_C = property(*K4Base.func_template(17, mask=0b1111111))
    send2_C = property(*K4Base.func_template(18, mask=0b1111111))

    pan_D = property(*K4Base.func_template(19, mask=0b11111, correct=-8))
    send1_D = property(*K4Base.func_template(20, mask=0b1111111))
    send2_D = property(*K4Base.func_template(21, mask=0b1111111))

    pan_E = property(*K4Base.func_template(22, mask=0b11111, correct=-8))
    send1_E = property(*K4Base.func_template(23, mask=0b1111111))
    send2_E = property(*K4Base.func_template(24, mask=0b1111111))

    pan_F = property(*K4Base.func_template(25, mask=0b11111, correct=-8))
    send1_F = property(*K4Base.func_template(26, mask=0b1111111))
    send2_F = property(*K4Base.func_template(27, mask=0b1111111))

    pan_G = property(*K4Base.func_template(28, mask=0b11111, correct=-8))
    send1_G = property(*K4Base.func_template(29, mask=0b1111111))
    send2_G = property(*K4Base.func_template(30, mask=0b1111111))

    pan_H = property(*K4Base.func_template(31, mask=0b11111, correct=-8))
    send1_H = property(*K4Base.func_template(32, mask=0b1111111))
    send2_H = property(*K4Base.func_template(33, mask=0b1111111))

    