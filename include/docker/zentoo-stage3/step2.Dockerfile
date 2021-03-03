FROM scratch

WORKDIR /
COPY --from=zentoo-bootstrap:latest /gentoo /
CMD ["/bin/bash"]

