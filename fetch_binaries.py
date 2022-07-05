import yaml
import urllib.request
import tarfile
import os
import subprocess


with open('versions.yml') as vFile:
    # Load YAML File
    data    = yaml.safe_load(vFile)["components"]
    bin_dir =  "usr/local/bin/"

    for k, v in data.items():
        # Parse Download URL with good version
        download_url = v["download_url"].replace("VERSION", v["version"])

        # Set target filename
        filename = v["filename"]
        
        # Download binaries
        urllib.request.urlretrieve(download_url, filename="%s%s" % (bin_dir, filename))

        # Untar if needed
        if v["unarchive"] == True:
            mytar = tarfile.open('%s%s' % (bin_dir, filename))
            if k == "etcd":
                mytar.extract("etcd-%s-linux-amd64/etcd" % (v["version"]), path=bin_dir)
                mytar.extract("etcd-%s-linux-amd64/etcdctl" % (v["version"]), path=bin_dir)
            elif k == "containerd":
                mytar.extract("bin/containerd", path=bin_dir)
                mytar.extract("bin/ctr", path=bin_dir)
                mytar.extract("bin/containerd-shim-runc-v2", path=bin_dir)
            else:
                mytar.extract(v["file_to_extract"], path=bin_dir)
            mytar.close()
            os.remove('%s%s' % (bin_dir, filename))

    # Cleanup unused dirs and compact
    os.system('sh scripts/cleanup.sh')
    
    with tarfile.open("binaries.tar.gz", "w:gz") as mytar:
        for k, v in data.items():
            ## Create tar file
            if k == "etcd":
                mytar.add("%s/etcd" % (bin_dir))
                mytar.add("%s/etcdctl" % (bin_dir))
            elif k == "containerd":
                mytar.add("%s/containerd" % (bin_dir))
                mytar.add("%s/ctr" % (bin_dir))
                mytar.add("%s/containerd-shim-runc-v2" % (bin_dir))
            else:
                mytar.add("%s/%s" % (bin_dir, k))
        mytar.close()