
import argparse
import sys 

from kontogu import core 


def cmd_test():
    print('here cmd test')
    pass

def cmd_hello():
    print('here cmd hello')
    pass

def execute():
    try:
        args = sys.argv
        if len(args) < 2:
            #_print_commands()
            #check_new_version()
            return

        command = args.pop(1)
        if command == "test":
            cmd_test()
        elif command == "hello":
            cmd_hello()
        elif command == "startup":
            core.startup()
        else:
            #_print_commands()
            print('command error')
    except KeyboardInterrupt:
        pass

    check_new_version()


if __name__ == "__main__":
    execute()