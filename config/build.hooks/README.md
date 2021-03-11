In this folder are definitions for build-time hooks. This system is completely optional; you can generate proper stages without anything written here. The seven directories where you actually enter definitions are:

(Happems outside chroot)
- ``0-copy``: Stuff that gets copied into the chroot prior to use. Uses rsync.

(Happens inside chroot)
- ``1-premerge``: Scripts that run prior to the ``emerge --unmerge`` operation. Remember, package configuration should be done via ``config/package.sets`` and ``config/package.flags``...
- ``2-unmerge``: A list of packages that need unmerging.
- ``3-postmerge``: Happens after ``emerge --unmerge``.
- ``4-services``: These services will be added to our base system, for a given runlevel. Also allows setting custom runlevels. At present, only OpenRC is supported but SystemD is a dim possibility in the distant future.

(Happens outside chroot)
- ``5-rm``: Removes individual files.
- ``6-empty``: rm -rf's entire subdirectories, using root privileges.

Finally, in ``tuple.defines`` we assemble our subset of hooks and refer to that handle, instead of having to assemble a multipart list every time.

Notes:
- The number prefixed to the subdirectly indicates its place in the sequence of activities.
- Hierachical/recursive definitions were strongly considered; I ultimately decided against them as we already get to use sets, and didn't want to duplicate the functionality. At some point this may change!
- Should you need to share scripts/data between hooks, place them into ``config/user-data`` and they'll be mounted under ``/mnt/user-data`` in the dockerized stage3. They'll also be available mounted in the installation chroot under the same directory name.
- Steps 1, 2, 3 are commands and these can get directly executed from the shell; order matters. Steps 0, 4, 5, 6 are lists and they get redundant items removed. To prevent surprises, use-flags are checked to see whether or not we have them both set and unset. Even if Portage handles them in last-in priority, our multi-build pipeline would otherwise silently create unexpected configurations by virtue of managing multiple configs. Performing the test and throwing up an error allows the user to fix any ambiguity.
- We will soon be supporting the set keyword ``@``, so please consider it reserved.
