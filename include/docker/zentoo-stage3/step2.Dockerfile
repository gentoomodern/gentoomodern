# This required, as Docker on Alpine currently seems to break without a local registry.
# As mentioned in the other file, having a local registry is a poor idea for this kind of scripted work. 

FROM scratch

WORKDIR /
COPY --from=zentoo-bootstrap:latest /gentoo /
CMD ["/bin/bash"]

