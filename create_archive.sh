#!/bin/bash


dirname=$(pwd)
cd ..
shopt -s extglob           
result=${dirname%%+(/)}    
result=${result##*/}       
printf '%s\n' "$result"


tar --exclude='.git' -cvf $result.tar.gz -C $result .
cp $result.tar.gz $result/$result.tar.gz
rm $result.tar.gz
cd $result
echo $result