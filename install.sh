#!/bin/bash

# Package installation
echo -e "\nChecking for dependencies, installing if necessary..."

cat requirements.txt | xargs sudo apt-get install -y 
