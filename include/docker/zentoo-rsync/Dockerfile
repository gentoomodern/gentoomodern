FROM alpine:latest

RUN apk update && apk add rsync

RUN mkdir -p /var/db/repos/gentoo && rm /etc/rsyncd.conf
