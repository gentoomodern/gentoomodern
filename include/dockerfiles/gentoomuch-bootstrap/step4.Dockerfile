# This required, as Docker on Alpine currently seems to break without a local registry.
# As mentioned in the other file, having a local registry is a poor idea for this kind of scripted work. 

FROM scratch

WORKDIR /
COPY --from=gentoomuch-bootstrap /gentoo /
RUN mkdir /mnt/stages \
&& mkdir /mnt/kernels \
&& mkdir /mnt/user-data \
&& mkdir /mnt/data-out \
&& mkdir /mnt/squashed-portage \
&& rm -rf /etc/portage/package.use \
&& mkdir /etc/portage/repos.conf \
&& mkdir /etc/portage/sets \
&& mkdir /etc/portage/patches
CMD ["/bin/bash"]

