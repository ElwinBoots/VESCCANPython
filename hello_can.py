#!/usr/bin/env python3
"""
 Created on Fri Nov 15 2024

 Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import can


def main():
    # Set up CAN interface
    bus = can.interface.Bus(channel="can0", bustype="socketcan")

    print("Listening for VESC CAN messages...")

    while True:
        message = bus.recv()
        if message is not None:
            print(
                f"Received CAN message: ID={message.arbitration_id}, Data={message.data}"
            )


if __name__ == "__main__":
    main()
