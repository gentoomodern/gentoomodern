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
- ``6-empty``: rm -rf's entire subdirectories, with root privileges.

Finally, in ``tuple.defines`` we assemble our subset of hooks and refer to that handle, instead of having to assemble a multipart list every time.

Notes:
- The number prefixed to the subdirectly indicates its place in the sequence of activities.
- Hierachical/recursive definitions were strongly considered; I ultimately decided against them as we already get to use sets.
- Should you need to share scripts/data between hooks, place them into the ``config/user-data`` and they'll be mounted under ``/mnt/user-data`` in the dockerized stage3. They'll also be available mounted in the install chroot under that same directory...
- Steps 1, 2, 3 are commands and these can get directly executed from the shell; order matters. Steps 0, 4, 5, 6 are lists and they get redundant items removed.
- We also support loading of newline-separated lists in order to support dynamically-generated content. You can also place them into ``config/user-data`` as above, to have them be sourced in another list by using ``. /mnt/user-data/my-subdirectory/my-list``. However, we do _not_ support the synomymous ``source`` keyword, so as not to clash with any possible end-users' configs.
- Inspired by Portage, the set specifier ``@`` is parsed by our tools and recognized here. For non-idempotent scripts, the order in which these sets get used matters. However, lists merely get their items tested for redundancy prior to having used.


```

```
