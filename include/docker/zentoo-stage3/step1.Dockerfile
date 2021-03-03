# This was adapted from stage3.Dockerfile from https://www.github.com/gentoo/gentoo-docker-images
# It does not support any of the dockerx-related code, as I've found it to break a lot, unpredictably.
# Also, mulltistage builds seem to require a local registry, which is very poor practice for our use-case as we need transient, hyper-localized build artifacts

FROM alpine:latest

WORKDIR /gentoo

ARG ARCH
ARG MICROARCH
ARG SUFFIX
ARG DIST="https://ftp-osl.osuosl.org/pub/gentoo/releases/${ARCH}/autobuilds"
ARG SIGNING_KEY="0xBB572E0E2D182910"

RUN echo "Building Gentoo Container image for ${ARCH} ${SUFFIX} fetching from ${DIST}" \
&& apk --no-cache add ca-certificates gnupg tar wget xz \
&& STAGE3PATH="$(wget -O- "${DIST}/latest-stage3-${MICROARCH}${SUFFIX}.txt" | tail -n 1 | cut -f 1 -d ' ')" \
&& echo "STAGE3PATH:" $STAGE3PATH \
&& STAGE3="$(basename ${STAGE3PATH})" \
&& wget -q "${DIST}/${STAGE3PATH}" "${DIST}/${STAGE3PATH}.CONTENTS.gz" "${DIST}/${STAGE3PATH}.DIGESTS.asc" \
&& gpg --list-keys \
&& echo "honor-http-proxy" >> ~/.gnupg/dirmngr.conf \
&& echo "disable-ipv6" >> ~/.gnupg/dirmngr.conf \
&& gpg --keyserver hkps://keys.gentoo.org --recv-keys ${SIGNING_KEY} \
&& gpg --verify "${STAGE3}.DIGESTS.asc" \
&& awk '/# SHA512 HASH/{getline; print}' ${STAGE3}.DIGESTS.asc | sha512sum -c \
&& tar xpf "${STAGE3}" --xattrs-include='*.*' --numeric-owner \
&& ( sed -i -e 's/#rc_sys=""/rc_sys="docker"/g' etc/rc.conf 2>/dev/null || true ) \
&& echo 'UTC' > etc/timezone
