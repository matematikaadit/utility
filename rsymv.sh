#!/bin/bash

rsync -avP --remove-source-files "$@"
