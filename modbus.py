from pymodbus.client.sync import ModbusTcpClient, ModbusSocketFramer

import struct

int_to_bytes = struct.Struct(">H").pack

def bytes_as_float(u16s):
    b = bytes()
    for i in u16s:
        b += int_to_bytes(i)
    return struct.Struct(">f").unpack(b)[0]
def bytes_as_double(u16s):
    b = bytes()
    for i in u16s:
        b += int_to_bytes(i)
    return struct.Struct(">d").unpack(b)[0]


class ModbusClient(ModbusTcpClient):
    def __init__(self, host, port=502, framer=ModbusSocketFramer, **kwargs):
        super().__init__(host=host, port=port, framer=framer, **kwargs)
    
    def get_power(self):
        out = {}
        res = self.read_input_registers(0x1314, 2).registers
        out["3P"] = bytes_as_float(res)
        res = self.read_input_registers(0x1320, 3*2).registers
        out["P1"] = bytes_as_float(res[:2])
        out["P2"] = bytes_as_float(res[2:4])
        out["P3"] = bytes_as_float(res[4:6])
        
        return out
    
    def g3p(self):
        res = self.read_input_registers(0x1314, 2).registers
        return bytes_as_float(res)
    
    def get_acc_pow(self):
        out = {}
        
        res = self.read_input_registers(0x2000, 4).registers
        out["3EP"] = bytes_as_double(res)
        res = self.read_input_registers(0x1320, 3*4).registers
        out["EP1"] = bytes_as_double(res[:4])
        out["EP2"] = bytes_as_double(res[4:8])
        out["EP3"] = bytes_as_double(res[8:12])
        
        return out