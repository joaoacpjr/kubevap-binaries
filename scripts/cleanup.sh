#!/bin/bash

basedir="usr/local/bin/"

# move binaries from their original folder
for binary in etcd etcdctl containerd ctr helm;
do
    for b in $(find $basedir* -type f -name $binary);
        do mv $b $basedir;
    done
    
done

# remove empty folders
for dir in $(find $basedir* -type d);
do
    rm -rf $dir;
done

# Set exec permission
find $basedir -type f -exec chmod +x {} \;