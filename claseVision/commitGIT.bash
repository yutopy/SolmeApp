#!/bin/bash

# Usage : bash pushGIT.bash localname

# En caso que el usuario haya dejado el / al final de la carpeta
# se debe quitar.
localname=$( echo $1 | sed -e "s/\///g")
cd $localname

# Clean latex aux files
rm -fv *.log
rm -fv *.bbl
rm -fv *.blg
rm -fv *.aux
rm -fv *.synctex.gz
rm -fv main.pdf
rm -fv *.out
rm -fv *.toc

# que recuerde la clave por una hora
git config --local credential.helper 'cache --timeout=3600'
# push local version to remote git server
git config user.email "jorgeluismartinezv@gmail.com"
git config user.name "JorgeMartinez1"
git status
git add .
git commit -a -m "Local Edit by Jorge at `date`"
git push $localname master
