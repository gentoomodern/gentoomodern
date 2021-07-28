Here is a descriptions of the contents of the configurations folders. This should guide the user in explorating this toolkit. Alphabetically:
<pre>
build.hooks
</pre>
These files get run at specific points in the GentooModern build process.

<pre>
cpu.defines
</pre>
Here we put the "-march"-style variables, with a named cpu config of your choice.

<pre>
env
</pre>
Here we have information pertaining to the GentooModern environment; the system architecture, the uid/gid of the operating user, and upstream url info.

<pre>
kernel.defines
</pre>
Here we define kernels as a tuple: A kernel package suffix (gentoo, vanilla, etc) and a newline-separated list of kernel fragments, as found in kernel.locals. 

<pre>
kernel.locals
</pre>
Here is where you keep your named kernel fragments. Note: Such fragments could be the entire kernel config, if you really wanted.

<pre>
kernels.build
</pre>
We list the kernels we wish to build; these are found in kernel.defines

<pre>
package.sets
</pre>
We define sets as line-separated files of packages. There can be directories/subdirectories, but they are for categorization: The configurations do not inherit the parents..

<pre>
patch.profiles
</pre>
Here we allow an entire profile to be patched. This affords a manner of setting patches on globally, especially due to partially broken alternative libc support in upstream packages.

<pre>
portage.locals
</pre>
In here are named directories corresponding to a named fragment of a Portage directory. These are munged together by our tools.

<pre>
stage.defines
</pre>
Each stage is defined as a subdirectory, having in it files such as "cpu", "flags", "packages", and "patches". Self-explanatory.

<pre>
stages.build
</pre>
This file is a list of the stages that our pipeline will build.

<pre>
user.patches
</pre>
Here is where the patches we create using this tool will get saved.
