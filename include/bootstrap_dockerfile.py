#!/usr/bin/env python3


def bootstrap_dockerfile(tarball_name):
    results =  'FROM scratch\n'
    results += 'COPY --from=localhost:5000/gentoomuch-bootstrap:latest / /\n'
    results += 'COPY ' + tarball_name + ' /\n'
    results += 'WORKDIR /\n'
    results += 'RUN mkdir /mnt/stages \\\n'
    results += '&& mkdir /mnt/kernels \\\n'
    results += '&& mkdir /mnt/user-data \\\n'
    results += '&& mkdir /mnt/data-out \\\n'
    results += '&& mkdir /mnt/squashed-portage \\\n'
    results += 'mkdir /mnt/gentoo \\\n'
    results += '&& rm -rf /etc/portage/package.use\n'
    results += 'CMD /bin/bash'
    return results
