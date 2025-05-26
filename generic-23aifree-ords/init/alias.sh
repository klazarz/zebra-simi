#!/bin/bash

alias check='watch systemctl --user status user-podman.service'
alias stopp='systemctl --user stop user-podman.service && systemctl --user stop db-podman.service'
alias cleanup='systemctl --user stop user-podman.service && systemctl --user stop db-podman.service rm -rf compose2cloud/ ; rm -rf .config/systemd/user/ ; rm -rf .oci ; podman stop jupyterlab ; podman stop demo ; buildah rm --all ; podman system prune --all --force ;rm -rf ~/tmp ; systemctl --user daemon-reload'
