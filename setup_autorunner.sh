#!/bin/bash
sudo cp robotrunner.service /etc/systemd/system/robotrunner.service
sudo systemctl daemon-reload
sudo systemctl start robotrunner.service
sudo systemctl enable robotrunner.service
