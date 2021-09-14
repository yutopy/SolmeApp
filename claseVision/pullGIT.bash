#!/bin/bash

# Usage : bash pullGIT.bash localname

# En caso que el usuario haya dejado el / al final de la carpeta
# se debe quitar.
localname=$( echo $1 | sed -e "s/\///g")
cd $localname

# que recuerde la clave por una hora
git config --local credential.helper 'cache --timeout=3600'
# Pull files from remote git server
git pull $localname master

