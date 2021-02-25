I absolutely fell in love with Gentoo, and having the stages on Dockerhub only makes life easier. This dockerized buildsystem creates an optimized buildmaster from the publicly-available Gentoo stages. Feel free to use as a baseline for your own work. Happy sysadmin/devops/embedded/whatever you're doing!


Note: This docker-compose file creates volumes for:
``
/var/cache/binpkg
/var/cache/distfiles
/var/db/repos/gentoo
``
This thing is almost ready for use as a daily driver... More documentation coming soon!
