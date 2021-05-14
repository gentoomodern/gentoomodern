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
&& echo 'UTC' > ./etc/timezone
