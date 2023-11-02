
#!/bin/bash


# Überprüfen, ob cmatrix bereits installiert ist
if dpkg -l | grep -q cmatrix; then
  echo "cmatrix ist bereits installiert. Überspringe die Installation."
else
  # Installation von cmatrix
  sudo apt-get update
  sudo apt-get install -y cmatrix
fi
