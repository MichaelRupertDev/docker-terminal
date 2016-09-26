from subprocess import Popen, PIPE
import re
import shlex

def DockerException():
    pass

def ps():
    p = Popen(['docker', 'ps'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    containers = []
    for row in output.split('\n'):
        containers.append(re.split(" {3,}", row))
    containers.pop(0) # get rid of the header row
    containers.pop()
    return containers

def run(image, **settings):
    cmd = 'docker run -d {}'.format(image, image)
    p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.wait()
    if rc != 0:
        return str(output) + str(err)
    return output

def stop(cid, remove=False):
    cmd = 'docker stop {}'.format(cid)
    if remove:
        cmd += '&& docker rm {}'.format(cid)
    p = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return output
