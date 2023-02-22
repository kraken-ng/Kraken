import docker, tarfile, os

from lib.exception import CoreException
from lib.printer import print_info


def get_container(client, image):
    containers = client.containers.list()
    for container in containers:
        if container.attrs['Config']['Image'] == image:
            return container
    return

def image_exists(client, image):
    try:
        client.images.get(image)
        return True
    except docker.errors.ImageNotFound:
        return False

def copy_to(container, src, dst):
    cwd = os.getcwd()
    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()
    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)
    os.remove(src + '.tar')
    os.chdir(cwd)
    return

def copy_from(container, src, dst):
    try:
        cwd = os.getcwd()
        os.chdir(os.path.dirname(dst))
        dstname = os.path.basename(dst)
        srcname = os.path.basename(src)
        data, file_stat = container.get_archive(src)
        fd = open(dst + '.tar', "wb")
        for chunk in data:
            fd.write(chunk)
        fd.close()
        tar = tarfile.open(dst + '.tar', mode='r')    
        fileobj = tar.extractfile(srcname)
        if os.name != "nt":
            os.remove(dstname + '.tar')
        os.chdir(cwd)
        return fileobj.read()
    except Exception:
        os.chdir(cwd)
        return

def create_container(client, image):
    if not image_exists(client, image):
        print_info(f"Pulling image '{image}'. It may take a few minutes")
        try:
            client.images.pull(image)
        except Exception:
            raise CoreException(f"Can not pull image: '{image}'. Maybe there is no internet access?")

    container = get_container(client, image)
    if not container:
        print_info(f"Running container from image: '{image}'")
        container = client.containers.run(image, "tail -f /dev/null", detach=True, remove=True)
    return container

def get_docker_env():
    return docker.from_env()
