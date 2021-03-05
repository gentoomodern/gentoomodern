I absolutely fell in love with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by concensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. I originally switched to Gentoo because Ubuntu at the time was giving me so much grief with video drivers, and I never looked back. There are significant advantages in working with a tailored operating system as things tends to stay in harmony. However, unless carefully managed Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate.

Gentoo and DevOps just made a baby: Immutable infrastructure with Gentoo! Gentoo Linux has been cast as intimidating and error-prone. This toolkit aims to remove many of the error-related aspects by ensuring that all your builds are done from a known state, and by offering you a way to define multiple your systems by using set composition. Hopefully, Gentoo will become less intimidating once people aren't afraid of breaking their system!

This tool aims to pick up where Gentoo's Catalyst/Crossdev stop and where programming-in-the-large begins: It allows Gentoo users to reversibly try unknown use-flag combinations. It allows long-time developers another means to orchestrate their own build processes. It allows any user to be brave; if you use source control on your ``config`` directory, you builds are now reversible! It affords a richness to Portage or ebuild bug reports that would otherwise be left to guesswork. It gives sysadmins who must juggle entire networks a modern way to reduce technical debt.Zentoo is Gentoo with a paper-thin abstraction layer that builds/packs stages and kernels. We use Docker Compose (multinode Swarm coming very soon!) to maintain a clean working environment on every run. The software creates an optimized buildmaster (and soon, optional distcc workers!) from any of the publicly-available Gentoo stages.

Zentoo is Gentoo with a few default configurations and a paper-thin, easy-to-audit abstraction layer that groups packages and use-flags. It creates an optimized buildmaster (and very soon, optional distcc workers) from any of the publicly-available Gentoo stages. These are subsequently used to compile other packages. In fact, once you setup, you can pull up a stage3 environment with ``./freshroot`` and start merging packages right away. It'll keep the built ones and you won't have to recompile them from scratch again. How fun!

``Zen emphasizes`` rigorous self-restraint, meditation-practice, insight into the nature of mind and things, and the expression of this insight in daily life, especially for the benefit of others. (Adapted from Wikipedia.) I hope this toolkit mirrors these ideals: This form imposes enough restraint over your builds to keep them sane over extended periods of time. It is the result of long-time Gentoo practice and and constant meditation upon the nature of how people think and machines work. It is also made to be used in our day-to-day lives. Last, this is intended for the benefit of the public.

The Gentoo Project has existing tools for building stages, but these aren't really designed for production: Although excellent for their intended purposes, these development tools are ill-suited to the task of customizing a network's worth of installations. In fact, I believe this is a big reason people critize them; a slightly different tool with a slightly different focus is needed for their use-cases. Zentoo aims to be a production tool as much as a development system. Due to being inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to anyone who already uses it.

Packages are compiled with FEATURES="binpkg-multi-instance buildpkg", which allows a single package repository to be shared across all our Dockerized hosts. Hosts that assemble packages into stages3 aren't given write-access to the package repository and use "binpkg-only." This means we can order our builds to allow, for example, a glibc-based host to compile musl and uclibc versions of programs that wouldn't otherwise be available on their respective Portage profiles due to unmet build-time dependencies!

User tasks:
- Everything you touch is in the config directory; the rest is either an executable file, or documentation, or temporary. Also, all config subdirectories have within them another one called ``zentoo``. Changing anything in those might break your builds, so I don't recommend it. :)
- Further documentation is in the config directory. Our aforementioned ``zentoo`` folders are intended as both part of our pipeline's configuration and as working examples for a network administrator.

What's the catch? Nothing comes for free - If you are an existing Gentoo user asking whether or not using this tool is worth it, I will be upfront about the costs and (current) limitations:
- Your workflow will change a bit and you'll want to look at ``./config/README.md``. Mostly it'll mean creating subdirectories for sets of packages/flags and then defining your machines from these sets, instead of directly within ``/etc/portage``
- Our minimal tools will place them into a temporary portage directory that get used by the dockerized root that does the compiling.
- If you want to set flags for rapid testing, change them under ``work/portage``, but make certain to preserve them under their respective ``./config`` directory or you'll lose them!
- Compared to the benefits derived from major improvements to build-environment resilience, I believe these costs are minimal.
- I think this code generally represents best practices for maintaining multiple Gentoo systems. If this code gets upstreamed or officially recommended by the Gentoo project in order to help as many users with source-based Linux, it would be a great honour: Source-based is important.

Implementation details:

Our docker-compose file creates persistent volumes for:
```
/var/cache/binpkg
/var/cache/distfiles
/var/db/repos/gentoo
```

- While still in its first week of development, this tool has already proven a smoother and far more reliable experience than any of my past methods.
- It is currently being developed and tested on AMD/Intel systems but ARM support is coming soon.
- This toolkit is a little less straightforward than your standard three-tier webapp: For example, one complication is that our output targets aren't usually other Docker containers. As such this was an excellent excuse to learn Docker in-depth!
