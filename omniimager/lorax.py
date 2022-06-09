import os
import subprocess


def build_install_img(workdir, product, version, release, repo_files, config_options, logger):
    logger.debug('Create Anaconda installer image with Lorax ...')
    buildarch = '--buildarch=' + os.uname().machine
    iso_dir = workdir + '/iso'
    subprocess.run('rm -rf ' + iso_dir, shell=True)
    cmd = ['lorax', '--isfinal', '-p', product, '-v', version + release,
           '-r', release, '--sharedir', '/etc/omni-imager/80-openeuler',
           '--rootfs-size=4', buildarch, '--repo', repo_files, '--nomacboot',
           '--noupgrade', iso_dir, '> /var/log/omni-image/lorax.logfile 2>&1']
    subprocess.run(' '.join(cmd), shell=True)
    return iso_dir
