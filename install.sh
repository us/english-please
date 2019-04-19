#!/usr/bin/env bash

(crontab -l ; echo "0 */12 * * * $PWD/run_script.sh > englishplease") | crontab