from subprocess import Popen, getoutput
import time

def without_keys(d, *keys):
    return dict(filter(lambda key_value: key_value[0] not in keys, d.items()))

def bash(command):
    output = getoutput(command)
    return output

def run_cmd(cmd, success_words=None):
    fail = True
    while fail:
        output = bash(cmd)
        time.sleep(1)
        print(output)
        if success_words is None or len(success_words) == 0:
            fail = False
        for sw in success_words:
            if len(output.split(sw)) > 1:
                fail = False