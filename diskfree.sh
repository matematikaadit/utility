#!/bin/bash

df -h | sed -n '1p;\|dev/sda|p'
