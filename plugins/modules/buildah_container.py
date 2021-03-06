#!/usr/bin/python
# Copyright (c) 2020 RedHat, 2021 Markus Falb
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# flake8: noqa: E501

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: buildah_container
author:
  - "Sagi Shnaidman (@sshnaidm)"
  - "Markus Falb (@mafalb)"
version_added: '0.0.1'
short_description: Manage buildah containers
notes: []
description:
  - Create and remove Buildah containers.
requirements:
  - buildah
options:
  name:
    description:
      - Name of the container
    required: True
    type: str
  executable:
    description:
      - Path to C(buildah) executable if it is not in the C($PATH) on the
        machine running C(buildah)
    default: 'buildah'
    type: str
  state:
    description:
      - I(absent) - A container matching the specified name will be stopped and
        removed.
      - I(present) - Asserts the existence of a container matching the name and
        any provided configuration parameters. If no container matches the
        name, a container will be created. If a container matches the name but
        the provided configuration does not match, the container will be
        updated, if it can be. If it cannot be updated, it will be removed and
        re-created with the requested config. Image version will be taken into
        account when comparing configuration. Use the recreate option to force
        the re-creation of the matching container.
      - I(created) - same as I(present)
    type: str
    default: present
    choices:
      - absent
      - present
      - created
  image:
    description:
      - Repository path (or image name) and tag used to create the container.
        If an image is not found, the image will be pulled from the registry.
        If no tag is included, C(latest) will be used.
      - Can also be an image ID. If this is the case, the image is assumed to
        be available locally.
    type: str
  annotation:
    description:
      - Add an annotation to the container. The format is key value, multiple
        times.
    type: dict
  authfile:
    description:
      - Path of the authentication file. Default is
        ``${XDG_RUNTIME_DIR}/containers/auth.json``
        (Not available for remote commands) You can also override the default
        path of the authentication file by setting the ``REGISTRY_AUTH_FILE``
        environment variable. ``export REGISTRY_AUTH_FILE=path``
    type: path
  blkio_weight:
    description:
      - Block IO weight (relative weight) accepts a weight value between 10 and
        1000
    type: int
  blkio_weight_device:
    description:
      - Block IO weight (relative device weight, format DEVICE_NAME[:]WEIGHT).
    type: dict
  cap_add:
    description:
      - List of capabilities to add to the container.
    type: list
    elements: str
    aliases:
      - capabilities
  cap_drop:
    description:
      - List of capabilities to drop from the container.
    type: list
    elements: str
  cgroup_parent:
    description:
      - Path to cgroups under which the cgroup for the container will be
        created.
        If the path is not absolute, the path is considered to be relative to
        the cgroups path of the init process. Cgroups will be created if they
        do not already exist.
    type: path
  cgroupns:
    description:
      - Path to cgroups under which the cgroup for the container will be
        created.
    type: str
  cgroups:
    description:
      - Determines whether the container will create CGroups.
        Valid values are enabled and disabled, which the default being enabled.
        The disabled option will force the container to not create CGroups,
        and thus conflicts with CGroup options cgroupns and cgroup-parent.
    type: str
  cidfile:
    description:
      - Write the container ID to the file
    type: path
  command:
    description:
      - Override command of container. Can be a string or a list.
    type: raw
  debug:
    description:
      - Return additional information which can be helpful for investigations.
    type: bool
    default: False
  env:
    description:
      - Set environment variables.
        This option allows you to specify arbitrary environment variables that
        are available for the process that will be launched inside of the
        container.
    type: dict
  podman_executable:
    description:
      - Path to C(podman) executable if it is not in the C($PATH) on the
        machine running C(buildah)
    default: 'podman'
    type: str
  workdir:
    description:
      - Working directory inside the container.
        The default working directory for running binaries within a container
        is the root directory (/).
    type: str
    aliases:
      - working_dir
"""

EXAMPLES = r"""
- name: Create a buildah container
  mafalb.containers.buildah_container:
    name: ci-rocky8
    image: quay.io/rockylinux/rockylinux:8
    state: present

- name: Remove a buildah container
  mafalb.containers.buildah_container:
    name: ci-rocky8
    state: absent
"""

RETURN = r"""
container:
    description:
      - Facts representing the current state of the container. Matches the
        buildah inspect output.
      - Note that facts are part of the registered vars since Ansible 2.8. For
        compatibility reasons, the facts
        are also accessible directly as C(buildah_container). Note that the
        returned fact will be removed in Ansible 2.12.
      - Empty if C(state) is I(absent).
    returned: always
    type: dict
    sample: '{
        "actions": [
            "recreated container"
        ],
        "buildah_actions": [
            "buildah rm container",
            "buildah --name container --cap-drop CAP_SYS_ADMIN from hello-world"
        ],
        "changed": true,
        "container": {
            "AddCapabilities": [],
            "CNIConfigDir": "/etc/cni/net.d",
            "CNIPluginPath": "/usr/libexec/cni:/opt/cni/bin",
            "Config": "{\"architecture\":\"amd64\", ...}",
            "ConfigureNetwork": "NetworkDefault",
            "Container": "container2",
            "ContainerID": "...",
            "DefaultCapabilities": [
                "CAP_AUDIT_WRITE",
                ...
            ],
            "DefaultMountsFilePath": "",
            "Devices": [],
            "Docker": {
                "architecture": "amd64",
                "config": {
                    "ArgsEscaped": true,
                    "AttachStderr": false,
                    "AttachStdin": false,
                    "AttachStdout": false,
                    "Cmd": [
                        "/bin/sh"
                    ],
                    "Domainname": "",
                    "Entrypoint": null,
                    "Env": [
                        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                    ],
                    "Hostname": "",
                    "Image": "sha256:...",
                    "Labels": null,
                    "OnBuild": [],
                    "OpenStdin": false,
                    "StdinOnce": false,
                    "Tty": false,
                    "User": "",
                    "Volumes": null,
                    "WorkingDir": ""
                },
                "container": "...",
                "container_config": {
                    "ArgsEscaped": true,
                    "AttachStderr": false,
                    "AttachStdin": false,
                    "AttachStdout": false,
                    "Cmd": [
                        "/bin/sh"
                    ],
                    "Domainname": "",
                    "Entrypoint": null,
                    "Env": [
                        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                    ],
                    "Hostname": "",
                    "Image": "sha256:...",
                    "Labels": null,
                    "OnBuild": [],
                    "OpenStdin": false,
                    "StdinOnce": false,
                    "Tty": false,
                    "User": "",
                    "Volumes": null,
                    "WorkingDir": ""
                },
                "created": "2019-03-07T22:19:53.447205048Z",
                "history": [
                    ...
                ],
                "os": "linux",
                "rootfs": {
                    "diff_ids": [
                        "sha256:..."
                    ],
                    "type": "layers"
                }
            },
            "DropCapabilities": [],
            "FromImage": "...",
            "FromImageDigest": "sha256:...",
            "FromImageID": "...",
            "History": [
                ...
            ],
            "IDMappingOptions": {
                "GIDMap": [],
                "HostGIDMapping": true,
                "HostUIDMapping": true,
                "UIDMap": []
            },
            "ImageAnnotations": null,
            "ImageCreatedBy": "",
            "Isolation": "IsolationOCIRootless",
            "Manifest": "{\n   \"schemaVersion\": 2,\n   ...}",
            "MountLabel": "system_u:object_r:svirt_sandbox_file_t:s0:c295,c943",
            "MountPoint": "",
            "NamespaceOptions": [
                {
                    "Host": true,
                    "Name": "cgroup",
                    "Path": ""
                },
                {
                    "Host": false,
                    "Name": "ipc",
                    "Path": ""
                },
                {
                    "Host": false,
                    "Name": "mount",
                    "Path": ""
                },
                {
                    "Host": true,
                    "Name": "network",
                    "Path": ""
                },
                {
                    "Host": false,
                    "Name": "pid",
                    "Path": ""
                },
                {
                    "Host": true,
                    "Name": "user",
                    "Path": ""
                },
                {
                    "Host": false,
                    "Name": "uts",
                    "Path": ""
                }
            ],
            "OCIv1": {
                "architecture": "amd64",
                "config": {
                    "Cmd": [
                        "/bin/sh"
                    ],
                    "Env": [
                        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
                    ]
                },
                "created": "2019-03-07T22:19:53.447205048Z",
                "history": [
                    ...
                ],
                "os": "linux",
                "rootfs": {
                    "diff_ids": [
                        "sha256:..."
                    ],
                    "type": "layers"
                }
            },
            "ProcessLabel": "system_u:system_r:svirt_lxc_net_t:s0:c295,c943",
            "Type": "buildah 0.0.1"
        },
        "failed": false,
        "stderr": "",
        "stderr_lines": [],
        "stdout": "container2\n",
        "stdout_lines": [
            "container2"
        ]
    }'
"""

from ansible.module_utils.basic import AnsibleModule  # noqa: E402
from ansible_collections.mafalb.containers.plugins.module_utils.buildah.buildah_container_lib import BuildahManager  # noqa: E402
from ansible_collections.mafalb.containers.plugins.module_utils.buildah.buildah_container_lib import ARGUMENTS_SPEC_CONTAINER  # noqa: E402


def main():
    module = AnsibleModule(
        argument_spec=ARGUMENTS_SPEC_CONTAINER,
        supports_check_mode=True,
    )

    # work on input vars
    if (module.params['state'] in ['present', 'created']
            and not module.params['image']):
        module.fail_json(msg="State '%s' requires image to be configured!" %
                             module.params['state'])

    # older buildah needs cap_ prefix in capability names
    if module.params['cap_add']:
        module.params['cap_add'] = [cap.upper() if cap.lower().startswith('cap_')
                                    else 'CAP_' + cap.upper()
                                    for cap in module.params['cap_add']]
    if module.params['cap_drop']:
        module.params['cap_drop'] = [cap.upper() if cap.lower().startswith('cap_')
                                     else 'CAP_' + cap.upper()
                                     for cap in module.params['cap_drop']]

    # newer buildah complains if a capability is both added and
    # dropped. Don't let that happen.
    if module.params['cap_add'] and module.params['cap_drop']:
        for cap in module.params['cap_add']:
            if cap in module.params['cap_drop']:
                module.fail_json(msg="capability '%s' cannot be dropped"
                                 " and added!" % cap)

    results = BuildahManager(module, module.params).execute()
    module.exit_json(**results)


if __name__ == '__main__':
    main()
