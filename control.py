#!/usr/bin/env python3
import can
import struct
import time
from typing import Optional

NODE_ID = 67

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

    def set_pos_floatingpoint(self, controller_id: int, pos: float , vel: float = 0) -> None:
        data = struct.pack(">f", pos ) 
        if vel > 0:
          data = data + struct.pack(">f", vel )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (68 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def set_velocity(self, controller_id: int, vel: float) -> None:
        data = struct.pack(">f", vel )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (69 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")


    def set_acceleration(self, controller_id: int, acel: float) -> None:
        data = struct.pack(">f", acel )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (70 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")


    def set_deceleration(self, controller_id: int, decel: float) -> None:
        data = struct.pack(">f", decel )

        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (71 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")
            
    def set_curpos(self, controller_id: int, pos: float , store : bool = 0 ) -> None:
        data = struct.pack(">f", pos )
        data = data + struct.pack(">b", store )


        # Create a CAN message with extended ID
        msg = can.Message(
            arbitration_id=(controller_id | (72 << 8)),  # 
            is_extended_id=True,
            data=data,  # No padding necessary for this command
        )

        # Send the CAN message
        try:
            self.bus.send(msg)
            print(f"Message sent: {msg}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def close(self):
        """
        Close the CAN bus connection.
        """
        self.bus.shutdown()


def main():
    controller = VescController()

    try:
        controller.set_velocity(NODE_ID, 70)
        controller.set_acceleration(NODE_ID, 200)
        controller.set_deceleration(NODE_ID, 50)
        # controller.set_curpos(NODE_ID, 0)
        controller.set_pos_floatingpoint( NODE_ID, 5 )


    except KeyboardInterrupt:
        print("\nStopping motor...")
    finally:
        # controller.send_current(NODE_ID, 0)  # Safety stop
        controller.close()


if __name__ == "__main__":
    main()
