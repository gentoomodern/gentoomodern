# This required, as Docker on Alpine currently seems to break without a local registry.
# As mentioned in the other file, having a local registry is a poor idea for this kind of scripted work.
# We may very well replace this mechanism with our own Dockerized images, as munging all this seems complicated and none too pleasant to justify in a code audit if one can simply not have i it present..
FROM scratch

COPY --from=gentoomuch-bootstrap:latest gentoo /
WORKDIR /
#SHELL ["/bin/bash", "-c"]
RUN mkdir /mnt/stages \
&& mkdir /mnt/kernels \
&& mkdir /mnt/user-data \
&& mkdir /mnt/data-out \
&& mkdir /mnt/squashed-portage \
&& mkdir /mnt/gentoo \
&& rm -rf /etc/portage/package.use \
&& mkdir /etc/portage/repos.conf \
&& mkdir /etc/portage/sets \
&& mkdir /etc/portage/patches 
