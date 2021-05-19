# This was adapted from stage3.Dockerfile from https://www.github.com/gentoo/gentoo-docker-images.
# The main difference is that the downloaded, verified stage3 is NOT deleted; we use it to seed another chroot.
# It also removes all BuildKit/buildx-related code, as it constantly breaks.
# Furthermore, multistage builds seem to require a local registry, which is very poor practice for our use-case:  We need transient, hyper-localized build artifacts.

FROM alpine:latest

WORKDIR /gentoo

ARG ARCH
ARG MICROARCH
ARG SUFFIX
ARG DIST="https://ftp-osl.osuosl.org/pub/gentoo/releases/${ARCH}/autobuilds"
ARG SIGNING_KEY="0xBB572E0E2D182910"

RUN echo "Building Gentoo Container image for ${ARCH} ${SUFFIX} fetching from ${DIST}" \
&& apk --no-cache add ca-certificates gnupg tar wget xz \
