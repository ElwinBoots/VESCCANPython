import can
from dataclasses import dataclass
from enum import IntEnum
import struct
from typing import Optional


class CanPacketId(IntEnum):
    STATUS = 9
    STATUS_2 = 14
    STATUS_3 = 15
    STATUS_4 = 16
    STATUS_5 = 27
    STATUS_6 = 28


@dataclass
class CanFrame:
    id: int
    data: bytes

    @property
    def vesc_id(self) -> int:
        return self.id & 0xFF

    @property
    def command_id(self) -> int:
        return (self.id >> 8) & 0xFF


class VescDecoder:
    @staticmethod
    def decode_status(frame: CanFrame) -> dict:
        erpm = struct.unpack(">i", frame.data[0:4])[0]
        current = struct.unpack(">h", frame.data[4:6])[0] / 10
        duty = struct.unpack(">h", frame.data[6:8])[0] / 1000
        return {"erpm": erpm, "current": current, "duty_cycle": duty}

    @staticmethod
    def decode_status_2(frame: CanFrame) -> dict:
        ah = struct.unpack(">i", frame.data[0:4])[0] / 10000
        ah_charged = struct.unpack(">i", frame.data[4:8])[0] / 10000
        return {"amp_hours": ah, "amp_hours_charged": ah_charged}

    @staticmethod
    def decode_status_3(frame: CanFrame) -> dict:
        wh = struct.unpack(">i", frame.data[0:4])[0] / 10000
        wh_charged = struct.unpack(">i", frame.data[4:8])[0] / 10000
        return {"watt_hours": wh, "watt_hours_charged": wh_charged}

    @staticmethod
    def decode_status_4(frame: CanFrame) -> dict:
        temp_fet = struct.unpack(">h", frame.data[0:2])[0] / 10
        temp_motor = struct.unpack(">h", frame.data[2:4])[0] / 10
        current_in = struct.unpack(">h", frame.data[4:6])[0] / 10
        pid_pos = struct.unpack(">h", frame.data[6:8])[0] / 50
        return {
            "temp_fet": temp_fet,
            "temp_motor": temp_motor,
            "current_in": current_in,
            "pid_pos": pid_pos,
        }

    @staticmethod
    def decode_status_5(frame: CanFrame) -> dict:
        tach = struct.unpack(">i", frame.data[0:4])[0] / 6
        voltage = struct.unpack(">h", frame.data[4:6])[0] / 10
        return {"tachometer": tach, "voltage_in": voltage}

    @staticmethod
    def decode_status_6(frame: CanFrame) -> dict:
        adc1 = struct.unpack(">h", frame.data[0:2])[0] / 1000
        adc2 = struct.unpack(">h", frame.data[2:4])[0] / 1000
        adc3 = struct.unpack(">h", frame.data[4:6])[0] / 1000
        ppm = struct.unpack(">h", frame.data[6:8])[0] / 1000
        return {"adc1": adc1, "adc2": adc2, "adc3": adc3, "ppm": ppm}

    @classmethod
    def decode(cls, frame: CanFrame) -> Optional[dict]:
        decoders = {
            CanPacketId.STATUS: cls.decode_status,
            CanPacketId.STATUS_2: cls.decode_status_2,
            CanPacketId.STATUS_3: cls.decode_status_3,
            CanPacketId.STATUS_4: cls.decode_status_4,
            CanPacketId.STATUS_5: cls.decode_status_5,
            CanPacketId.STATUS_6: cls.decode_status_6,
        }

        decoder = decoders.get(frame.command_id)
        if decoder:
            result = decoder(frame)
            result["vesc_id"] = frame.vesc_id
            return result
        return None


def main():
    # Configure the CAN interface
    # bus = can.Bus(channel="PCAN_USBBUS1", interface="socketcan")
    bus = can.Bus(channel="PCAN_USBBUS1", interface = 'pcan')
    # import usb

    # dev = usb.core.find(idVendor=0x1D50, idProduct=0x606F)
    # bus = can.Bus(interface="gs_usb", channel="PCAN_USBBUS1", index=0, bitrate=500000)
    # bus = can.Bus(interface="gs_usb", channel=dev.product, bitrate=500000)
    
    print("Listening for VESC CAN messages...")

    try:
        while True:
            message = bus.recv()
            if message.is_extended_id:
                frame = CanFrame(message.arbitration_id, message.data)
                result = VescDecoder.decode(frame)
                if result:
                    print("\nReceived message:")
                    print(f"VESC ID: {result.pop('vesc_id')}")
                    for key, value in result.items():
                        print(f"{key}: {value}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
