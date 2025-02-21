#!/usr/bin/env python3
import can
import struct
import time
from typing import Optional

NODE_ID = 31

class VescController:
    def __init__(self, can_channel: str = "can0", bitrate: int = 500000):
        """
        Initialize the VESC Controller.

        Args:
            can_channel (str): CAN channel (default: "can0").
            bitrate (int): CAN bus bitrate in bits per second (default: 500000).
        """
        # self.bus = can.Bus(channel=can_channel, interface="socketcan", bitrate=bitrate)
        self.bus = can.Bus(channel="PCAN_USBBUS1", interface = 'pcan')

    def send_current(self, controller_id: int, current: float) -> None:
        """
        Send a command to set the motor current for a VESC.

        Args:
            controller_id (int): VESC ID (0-255).
            current (float): Desired current in amperes (-MOTOR_MAX to MOTOR_MAX).
        """
        # Scale the current to a 32-bit integer with scaling factor 1000
        current_scaled = int(current * 1000)

        # Pack the scaled current into 4 bytes (big-endian, signed)
        data = struct.pack(">i", current_scaled)

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (0x01 << 8)),  # Command ID 1 (SET_CURRENT)
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def set_rpm(self, controller_id: int, rpm: float) -> None:

        # Pack the scaled current into 4 bytes (big-endian, signed)
        data = struct.pack(">i", rpm)

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (0x03 << 8)),  # Command ID 3 (SET_RPM)
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def set_pos(self, controller_id: int, pos: float) -> None:

        # Pack the scaled current into 4 bytes (big-endian, signed)
        data = struct.pack(">i", int(pos * 1000000.0))

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (0x04 << 8)),  # Command ID 4 (SET_POS)
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")
            
    def set_kp(self, controller_id: int, kp: float) -> None:
        data = struct.pack(">f", kp )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (64 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def set_ki(self, controller_id: int, ki: float) -> None:
        data = struct.pack(">f", ki )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (65 << 8)),  #
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def set_kd(self, controller_id: int, kd: float) -> None:
        data = struct.pack(">f", kd )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (66 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def set_pos_elwin(self, controller_id: int, pos: float) -> None:
        data = struct.pack(">f", pos )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (68 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

    def close(self):
        """
        Close the CAN bus connection.
        """
        self.bus.shutdown()


def main():
    controller = VescController()

    try:
        # controller.set_pos_elwin(NODE_ID, 0)
        scale = 1
        # time.sleep(0.5)
        # controller.set_pos(NODE_ID, 0)
        # time.sleep(0.5)
        controller.set_pos_elwin( NODE_ID, 360*1*scale )
        time.sleep(0.5)
        controller.set_pos_elwin( NODE_ID, 360*0*scale )
        time.sleep(0.5)
        controller.set_pos_elwin( NODE_ID, 180*scale )
        time.sleep(0.5)
        controller.set_pos_elwin( NODE_ID, 540*scale )
        time.sleep(0.5)
        controller.set_pos_elwin( NODE_ID, 0*scale )

        # controller.set_rpm(NODE_ID, 1000)
        # time.sleep(0.5)
        # controller.set_rpm(NODE_ID, 1000)
        # time.sleep(0.5)
        # controller.set_rpm(NODE_ID, 2000)
        # time.sleep(0.5)
        # controller.set_rpm(NODE_ID, 2000)
        # time.sleep(0.5)
        # print("Ramping up current...")
        # for i in range(5):  # Ramp up to 5A
        #     current = (i + 1)/5
        #     print(f"Setting current to {current}A")
        #     controller.send_current(NODE_ID, current)
        #     time.sleep(0.5)

        # print("Ramping down...")
        # for i in range(5):  # Ramp down to 0
        #     current = (5 - i - 1)/5
        #     print(f"Setting current to {current}A")
        #     controller.send_current(NODE_ID, current)
        #     time.sleep(0.5)



        # scale = 1
        # controller.set_kp(NODE_ID , 0.05*scale)
        # controller.set_ki(NODE_ID , 0.0391*scale)
        # controller.set_kd(NODE_ID , 0.0031*scale)
        
        
        
        # scale = 1
        # controller.set_pos_elwin( NODE_ID, 360*1*scale )
        # time.sleep(0.5)
        # controller.set_pos_elwin( NODE_ID, 360*0*scale )
        # time.sleep(0.5)
        # controller.set_pos_elwin( NODE_ID, 180*scale )
        # time.sleep(0.5)
        # controller.set_pos_elwin( NODE_ID, 540*scale )
        # time.sleep(0.5)
        # controller.set_pos_elwin( NODE_ID, 0*scale )

        # for i in range(360*10):
        #   controller.set_pos_elwin( NODE_ID, i )
        #   time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nStopping motor...")
    finally:
        # controller.send_current(NODE_ID, 0)  # Safety stop
        controller.close()


if __name__ == "__main__":
    main()
