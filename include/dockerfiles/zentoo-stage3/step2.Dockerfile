# This required, as Docker on Alpine currently seems to break without a local registry.
# As mentioned in the other file, having a local registry is a poor idea for this kind of scripted work. 

FROM scratch

WORKDIR /
COPY --from=zentoo-bootstrap /gentoo /
RUN mkdir /mnt/{stages, kernels, user-data, data-out} && \
	rm -rf /etc/portage/package.use
CMD ["/bin/bash"]

