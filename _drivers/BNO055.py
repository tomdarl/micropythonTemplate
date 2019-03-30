# changes from github example:
# 	added 600ms delay after reset to allow BNO055 to boot
# 	changed I2C from machine to pyb instance

import ustruct
from time import sleep_ms
import pyb

def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)
    return _partial

_CHIP_ID = 0xa0

CONFIG_MODE = 0x00
ACCONLY_MODE = 0x01
MAGONLY_MODE = 0x02
GYRONLY_MODE = 0x03
ACCMAG_MODE = 0x04
ACCGYRO_MODE = 0x05
MAGGYRO_MODE = 0x06
AMG_MODE = 0x07
IMUPLUS_MODE = 0x08
COMPASS_MODE = 0x09
M4G_MODE = 0x0a
NDOF_FMC_OFF_MODE = 0x0b
NDOF_MODE = 0x0c

_POWER_NORMAL = 0x00
_POWER_LOW = 0x01
_POWER_SUSPEND = 0x02


class BNO055:
    """
    Driver for the BNO055 9DOF IMU sensor.
    Example::
        import bno055
        from pyb import I2C
        i2c = I2C(2, pyb.I2C.MASTER)
        bno = bno055.BNO055(i2c)
        print(bno.temperature())
        print(bno.euler())
    """

    def __init__(self, i2c, address=0x28):
        self.i2c = i2c
        self.address = address
        self.init()

    def _registers(self, register, struct, value=None, scale=1):
        if value is None:
            size = ustruct.calcsize(struct)
            data = self.i2c.mem_read(size, self.address, register)
            value = ustruct.unpack(struct, data)
            if scale != 1:
                value = tuple(v * scale for v in value)
            return value
        if scale != 1:
            value = tuple(v / scale for v in value)
        data = ustruct.pack(struct, *value)
        self.i2c.mem_write(data, self.address, register)

    def _register(self, register, value=None, struct='B'):
        if value is None:
            return self._registers(register, struct=struct)[0]
        self._registers(register, struct=struct, value=(value,))

    _chip_id = partial(_register,
                       register=0x00,
                       value=None)

    _power_mode = partial(_register,
                          register=0x3e)

    _system_trigger = partial(_register,
                              register=0x3f)

    _page_id = partial(_register,
                       register=0x07)

    calibration = partial(_register,
                          register=0x35,
                          value=None)

    operation_mode = partial(_register,
                             register=0x3d)

    errorcode = partial(_register,
                        register=0x3a,
                        value=None)

    systemstatus = partial(_register,
                           register=0x39,
                           value=None)

    temperature = partial(_register,
                          register=0x34,
                          value=None)

    accelerometer = partial(_registers,
                            register=0x08,
                            struct='<hhh',
                            value=None,
                            scale=1 / 100)

    magnetometer = partial(_registers,
                           register=0x0e,
                           struct='<hhh',
                           value=None,
                           scale=1 / 16)

    gyroscope = partial(_registers,
                        register=0x14,
                        struct='<hhh',
                        value=None,
                        scale=1 / 900)

    euler = partial(_registers,
                    register=0x1a,
                    struct='<hhh',
                    value=None,
                    scale=1 / 16)

    quaternion = partial(_registers,
                         register=0x20,
                         struct='<hhhh',
                         value=None,
                         scale=1 / (1 << 14))

    linear_acceleration = partial(_registers,
                                  register=0x28,
                                  struct='<hhh',
                                  value=None,
                                  scale=1 / 100)

    gravity = partial(_registers,
                      register=0x2e,
                      struct='<hhh',
                      value=None,
                      scale=1 / 100)

    def init(self, mode=NDOF_MODE):
        chip_id = self._chip_id()
        if chip_id != _CHIP_ID:
            raise RuntimeError("bad chip id (%x != %x)" % (chip_id, _CHIP_ID))
        self.reset()
        self._power_mode(value=_POWER_NORMAL)
        self._page_id(value=0)
        self._system_trigger(value=0x00)
        self.operation_mode(value=mode)

    def reset(self):
        self.operation_mode(value=CONFIG_MODE)
        self._system_trigger(value=0x20)
        pyb.delay(600)  # added to avoid calling read within BNO reset period
        while True:
            try:
                chip_id = self._chip_id()
            except OSError as e:
                if e.args[0] != 19:  # errno 19 ENODEV
                    raise
                chip_id = 0
            if chip_id == _CHIP_ID:
                return

    def use_external_crystal(self, value):
        last_mode = self.operation_mode()
        self.operation_mode(value=CONFIG_MODE)
        self._page_id(value=0)
        self._system_trigger(value=0x80 if value else 0x00)
        self.operation_mode(value=last_mode)

    def fix_bno(self):
        rval = [-1, -1, -1]
        while ((rval[0] != NDOF_MODE) and (rval[1] != 5) and (rval[2] != 0)):
            self.operation_mode(value=NDOF_MODE)
            for i in range(4):
                sleep_ms(50)
                rval = self.operation_mode(), self.systemstatus(), self.errorcode(), self.temperature(), self.euler()
        return rval

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 syn=python
