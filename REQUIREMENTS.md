These are the high-level requirements for Gentoomuch.

1 - The software SHALL offer the  means for a user to define multiple Gentoo linux stages in a declarative manner.
2 - The software SHALL be able of running automated builds based on these definitions.
3 - The user's configuration SHALL be stored as text files. This is to enable version control.
4 - Each subset of configuration SHALL be in its own folder.
5 - The software SHALL assemble the desired subsets in a temporary environment.
6 - The software SHALL also offer a trivial manner of starting a baseline chroot, for live experimenting.
7 - Changes made in the chroot environment SHALL NOT propagate up to the user-defined configuration.
8 - Each function or method SHALL have its existence justified, and have both its usage and its code documented.
9 - Each class member variable SHALL be explained in code comments.
10 - End-user facing documentation SHALL be provided, with walkthroughs for all use-cases.
