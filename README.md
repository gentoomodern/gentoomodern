Note: Master branch only has initial work - almost everything is in dev; it will be merged within the next few days.

I absolutely fell in love with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by concensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. I originally switched to Gentoo because Ubuntu at the time was giving me so much grief with video drivers, and I never looked back. There are significant advantages in working with a tailored operating system as things tends to stay in harmony. However, unless carefully managed Gentoo is guaranteed to suffer from configuration drift.

The good news is that the Gentoo project has started offering stage3 images on Dockerhub. It's time for Gentoo and DevOps to make a baby: Let's implement immutable infrastructure with Gentoo!

Zentoo is Gentoo with an additional abstraction layer that builds and packages, and also a methodology: We use Docker Swarm to maintain a clean working environment, every single time. The software creates an optimized buildmaster (and optional distcc worker) from any of the publicly-available Gentoo stages. These are subsequently used to compile other packages. In fact, you can pull up a new stage3 environment with ./freshroot and start merging packages right away. The next time you get into an environment it'll keep the built package and you won't have te recompile it from scratch again. We mount a multi-instance binpkg repo and away we go! Coming soon will be automatic cleanup, repairs, and tmpfs caching for the best experience!

Zen, as emphasizes rigorous self-restraint, meditation-practice, insight into the nature of mind and things, and the expression of this insight in daily life, especially for the benefit of others. (Adapted from Wikipedia.)

This toolkit (hopefully) mirrors these ideals: This form imposes enough restraint over your builds to keep them sane over extended periods of time. It is the result of constant practice and meditation upon the nature of how people think and machines work, from which I fetched the insights needed to make these tools well-considered. Last, this is intended for the benefit of the public.   

This toolkit aims to pick up where Gentoo's Catalyst/Crossdev stop and the end-users' needs begin. The Gentoo Project has existing tools for building stages, but these aren't really designed for production: Although excellent for their intended purposes, these are ill-suited to the task of customizing a network's worth of installations. Zentoo aims to be a production tool as much as a development system. Due to being inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to anyone who already uses it.

Packages are compiled with FEATURES="binpkg-multi-instance buildpkg", which allows a single package repository to be shared across all hosts. Hosts that assemble aren't given write-access to the package repository and use "binpkg-only." This allows, for example, a glibc-based host to compile musl and uclibc versions of a tool that wouldn't otherwise be available on their respective Portage profiles due to unmet dependencies!

While still in its first few days of development, this tool has already proven a smoother and far more reliable experience than any of my past methods. it is currently being developed and tested on AMD/Intel systems but ARM support is coming soon. This toolkit is a little less straightforward than your standard three-tier webapp: For example, one complication is that our output targets aren't usually other Docker containers. As such this was an excellent excuse to learn Docker in-depth!

User tasks:

1) For each root, define your /etc/portage directory as a named branch in config/portage
2) If needed, define buildhooks as a named branch in config/buildhooks.
3) Define package sets in the config/portage/sets directory. https://wiki.gentoo.org/wiki/Package_sets#User_defined_sets
4) Define system tuples (``<cpu>-<portage>-<buildhooks>-<packages>>``) in config/tuples.

Something worth noting is that the first three tasks rely upon git branches, whereas the latter two do not. This is both because the first three's file hierarchies are duplicate, and also due to the fact that these settings only concern a single root at a time: As such our build system can checkout from a given branch, do its work, and restart with another. Also, these tend to be more widely-shared as they are used as building blocks to build a production network.

Furthermore, the latter two are not image-specific but represent the initial state of an entire network. Not only does that kind of information tend to be kept private, but the type kind of workflow is better-suited to the master-dev branch workflow instead of using git as a convenient key-value store for code configuration. However, there will be an option for building multiple sites.

Implementation details:

Our docker-compose file creates persistent volumes for:
```
/var/cache/binpkg
/var/cache/distfiles
/var/db/repos/gentoo
```
