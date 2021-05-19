<h2>GentooMuch:</h2><h3> Something like this was bound to happen...</h3>

<h3>Intro:</h3> I absolutely fell in love with Gentoo Linux several years ago. It is an amazing meta-distribution backed by a vibrant all-volunteer group of developers and maintainers who operate mostly by concensus. You can readily optimize a Gentoo system to obtain the best performance, reliability, and compatibility possible. I originally switched to Gentoo because Ubuntu at the time was giving me so much grief with video drivers, and I never looked back. There are significant advantages in working with a tailored operating system as things tends to stay in harmony. However, unless carefully managed Gentoo is guaranteed to suffer from configuration drift as patches and hacks accumulate. This toolkit helps greatly to provide such careful management.

<h3>GentooMuch is Gentoo + Docker with an orchestration layer</h3> that builds and packs stages and kernels. We use Docker-Compose (planning to transition to the Docker Python SDK) to maintain a clean working environment on every run. The software creates an optimized buildmaster (and soon, optional distcc workers!) from any of the publicly-available Gentoo stages.

The Gentoo Project has existing tools for repeatably building stages, but these aren't really designed for production: Although excellent for their intended purposes, these development tools are ill-suited to the task of customizing a network's worth of installations. In fact, I believe this is a big reason people can sometimes critize them; a slightly different tool with a slightly different focus is needed for their use-cases. GentooMuch aims to be a production tool as much as a development system. Due to being inspired by Gentoo's existing workflows, its patterns should be implicitly relatable to anyone who already uses it.

Gentoo and DevOps just made a baby: Immutable infrastructure with Gentoo! Gentoo Linux has been cast as intimidating and error-prone, and this toolkit aims to remove much of the related aspects by ensuring that all your builds are done from a known state, and by offering you a way to define multiple your systems by using set composition. Hopefully, Gentoo will become less intimidating once people aren't afraid of breaking their system!

GentooMuch allows Gentoo users to reversibly try unknown use-flag combinations. It allows long-time developers another means to orchestrate their own build processes. It allows any user to be brave; if you use source control on the ``config`` directory, then congratulations: your builds are now reversible! GentooMuch gives sysadmins who must juggle entire networks a modern way to reduce technical debt. It's a rather civilized way of managing multiple Gentoo installations.

<h3>This tool is just made to be played with.</h3> In fact, once you setup, you can pull up a stage3 environment with ``./freshroot`` and start merging packages right away! It'll keep the built ones and you won't have to recompile them from scratch again. How fun!

Packages are compiled (along others) with FEATURES="binpkg-multi-instance buildpkg", which allows a single package repository to be shared across all our Dockerized hosts. This minimized compilation used space! Hosts that assemble packages into stages3 aren't given write-access to the package repository and use "binpkg-only." This means (in theory) we can order our builds to allow, for example, a glibc-based host to compile musl and uclibc versions of programs that wouldn't otherwise be available on their respective Portage profiles due to unmet build-time dependencies!

User tasks:
- Everything you touch is in the config directory; the rest is either an executable file, or documentation, or temporary. Also, all config subdirectories have within them another one called ``gentoomuch``. Changing anything in those might break your builds, so I don't recommend it. :)
- Further documentation is in the config directory. Our aforementioned ``gentoomuch`` folders are intended as both part of our pipeline's configuration and as working examples for someone looking to get started.

What's the catch? Nothing comes for free - If you are an existing Gentoo user asking whether or not using this tool is worth it, I will be upfront about the costs and (current) limitations:
- While still in development, this tool has already proven a smoother and far more reliable experience than any of my past methods.
- It will munge these configs into a temporary portage directory that get used by the (dockerized) stage3 that compiles everything.
- If you want to set flags for rapid testing, feel free to spin up a temporary environment with ``./fresh-root`` and whatever you update in /etc/portage will show up under ``work/portage``, but make certain to preserve these configs under their respective ``./config`` directory or you'll lose them!
- Your workflow will change a bit and you'll want to look at ``./config/README.md``. Mostly it'll mean creating subdirectories for sets of packages/flags and then defining your machines from these sets, instead of directly within ``/etc/portage``
- Compared to the benefit of vastly superior resilience and manageability, these costs are minimal.
- I think this code generally represents best practices for maintaining multiple Gentoo systems; nothing is ever perfect but this toolkit is solid. If this code gets upstreamed or recommended by the Gentoo project, it would be a great honour: Source-based Linux is extremely important to me.
- GentooMuch is currently being developed and tested on AMD/Intel systems but ARM support is coming soon.
- Since this toolkit is a little less straightforward than a standard three-tier webapp, this project has been an excellent excuse to learn Docker in-depth!
