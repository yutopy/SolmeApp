#!/bin/bash

# Para crear el proyecto de form local :
# $1 es el nombre local del proyecto.
# $2 es el codigo GIT del proyecto en overleaf
# 

# Variables
login=jorgeluismartinezv@gmail.com

# Modificar el @ del email por %40
login=$(echo $login | sed -e "s/@/\%40/g")

# crear el folder
mkdir $1
cd $1
# que recuerde la clave por una hora
git config --local credential.helper 'cache --timeout=3600'
# Inicializar git en el folder local con la copia remota
git init
git remote add $1 https://$login@git.overleaf.com/$2
git pull $1 master

