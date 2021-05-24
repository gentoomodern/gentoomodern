#!/usr/bin/env python3
import os, sys


def pull_stage3(arch, profile)
    # These paths are used for working with our Dockerfile configs.
    dockerfile_input_path = 'include/dockerfiles/'
    dockerfile_output_path = 'work/bootstrap/'
    # Bootstrap Phase:
    # We can now append all the Dockerfiles for the bootstrap phase, using a different file given whether or not we use a custom tag.
    lines = read_file_lines(os.path.join(dockerfile_input_path, 'step1.Dockerfile'))
    if is_default_tag: # We don't have a custom tag.
        lines.extend(read_file_lines(os.path.join(dockerfile_input_path, 'step2.Dockerfile.archonly')))
    else: # We do have a custom tag. Hurray!
        lines.extend(read_file_lines(os.path.join(dockerfile_input_path, 'step2.Dockerfile.fully-loaded')))
    lines.extend(read_file_lines(os.path.join(dockerfile_input_path, 'step3.Dockerfile')))
    print(lines)
    # We create the output directory if it isn't present.
    if not os.path.isdir(dockerfile_output_path):
        os.mkdir(dockerfile_output_path)
    # Now we finally write the Dockerfile for the bootstrap image.
    write_file_lines(os.path.join(dockerfile_output_path, 'Dockerfile'), lines)
    # These two are for the error and debug messages'
    attempt_msg_prefix = 'gentoomuch.pull_stage(): Attempted to pull stage3 of arch "' 
    tag_msg = '", wih tag "' 
    # This is the image that gets used to build/pack by this tool.
    # The only purpose of the bootstrap Docker image is to download, verify, and unpack the upstream stage3. Then it gets copied from and destroyed.
    cleaned_profile = re.sub(re.escape('+'), '-', profile)
    # Names for images and stuff.
    bootstrap_img_name = 'gentoomuch-bootstrap'
    output_img_name = image_base_tag + arch + '-' + cleaned_profile + ':upstream'
    bootstrap_cmd_head = 'docker image rm ' + output_img_name + ' & docker image rm ' + bootstrap_img_name + ' & cd ' + dockerfile_output_path + ' && docker build '
    bootstrap_cmd_tail = ' -t gentoomuch-bootstrap .'
    # Now we set the command that gets run.
    common_args = '--build-arg ARCH=' + arch + ' --build-arg MICROARCH=' + arch
    #upstream_url_msg = " from custom upstream "
    if not profile == 'default': # If we have a custom tag.
        common_args = common_args + ' --build-arg SUFFIX=' + profile + ' '
        # print(attempt_msg_prefix + arch + tag_msg + tag + '" from gentoo\'s upstream')
    if custom_upstream: # If our upstream isn't the one defined in the Dockerfile.
        common_args = common_args + ' --build-arg DIST=' + upstream_url
    # We build the bootstrap image.
    code = os.system(bootstrap_cmd_head + common_args + bootstrap_cmd_tail)
    if code != 0:
        sys.exit('gentoomuch.pull_stage(): Bootstrap Docker image build failed.')
    # We then build the final output image (AKA: The value-added part we wrote this thing to do...)
    code = os.system('cp ' + os.path.join(dockerfile_input_path,'step4.Dockerfile') + ' ' + os.path.join(dockerfile_output_path,  'Dockerfile') + ' && cd ' + dockerfile_output_path + ' && docker build -t ' + output_img_name + ' .')
    if code != 0:
        sys.exit('gentoomuch.pull_stage(): Error code ' + str(code))
    # Removing bootstrap image...
    code = os.system('docker image rm -f ' + bootstrap_img_name)
    if code != 0:
        sys.exit('gentoomuch.pull_stage(): Could not remove temporary bootstrap image')
    # FINISHED


