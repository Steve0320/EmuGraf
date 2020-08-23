from emu_power import Emu
import argparse
import sys
import json

if __name__ == "__main__":

    # Arguments
    description = (
        "Connect to an EMU-2 device and output power data. This script is intended "
        "to be run in conjunction with the Telegraf execd input. A newline on stdin "
        "triggers output, as per the recommended execd spec."
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('port', help='Serial port that the EMU is attached to')
    parser.add_argument('--name', help='Name to use for the Telegraf measurement', default='emu')

    args = parser.parse_args()

    # Setup API. Note: setting schedule seems to be broken so
    # we issue the update commands manually
    api = Emu(synchronous=True)

    if not api.start_serial(args.port):
        print("Error: failed to open serial port")
        exit(1)

    while True:

        # Block until Telegraf signal
        sys.stdin.readline()

        demand = api.get_instantaneous_demand()
        summation = api.get_current_summation_delivered()

        output = {
            'name': args.name,
            'demand': demand.reading,
            'summation': summation.reading
        }

        print(json.dumps(output))
