Usage
======

1. Configure dockyard cli using `dcli configure`
2. Connect to dockyard workspace using `dcli ssh <workspace name>`
3. Transfer files/directories to/from workspace using `dcli scp <source> <target>`.

    a) source/target could be a local path (including .)

    b) source/target could be a remote relative path inside workspace directory `<workspace_name>:<path>`

    c) source/target could be a remote full path inside workspace `<workspace_name>:/<path>` or `<workspace_name>:~/<path>`

