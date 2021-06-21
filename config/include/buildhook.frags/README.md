here are where we place the actual scripts for our build-hooks (bash). Using this subsystem is completely optional; you can generate running systems without touching anything here. The directories where you actually enter definitions are:

(Happems outside chroot)
- ``0-copy``: Stuff that gets copied into the chroot prior to use. Uses rsync. (List of items)

(Happens inside chroot)
- ``1-premerge``: These run prior to unmerging. (Scripts/Executables)
- ``2-unmerge``: Packages that get unmerged, with warnings suppressed. (List of items)
- ``3-postmerge``: These run after unmerging (Scripts/Executables)
- ``4-services``: These services will be added to our base system at level default if not otherwise specified. At present, only OpenRC is supported. (List of items)

(Happens outside chroot)
- ``5-remove``: Removes files and folders; directories listed here get removed too! (List of items)


Notes:
- The number prefixed to the subdirectly indicates its place in the sequence of activities.
- Should you need to share scripts/data between hooks, place them into ``config/user-data`` and they'll be available mounted under ``/mnt/user-data`` in the build environment.
