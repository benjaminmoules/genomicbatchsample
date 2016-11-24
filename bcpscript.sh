#!/bin/bash

useradd -m bcos_calc
#echo "newpass" | passwd --stdin bcos_calc

su -l bcos_calc -c "mkdir /home/bcos_calc/bin /home/bcos_calc/data /home/bcos_calc/scripts /home/bcos_calc/lib /home/bcos_calc/jobdir"
#mkdir -m 0700 ~bcos_calc/.ssh
#touch ~bcos_calc/.ssh/authorized_keys
#chown bcos_calc:bcos_calc ~bcos_calc/.ssh ~bcos_calc/.ssh/authorized_keys
#su -l bcos_calc -c "chmod go-rwx ~bcos_calc/.ssh/authorized_keys"
#cp /root/.ssh/authorized_keys /home/bcos_calc/.ssh/authorized_keys

#yum -y install epel-release
apt-get install -y libprotobuf-c0 openssl

cd /home/bcos_calc/bin/
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bcd2bvcf' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bvcf_convert_and_filter' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bvcf_create_map' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bvcf_demultiplex' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bvcf_merge' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bvcf_multiplex' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bvcf_retrieve' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/bvcf_transpose' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/gPLINK.jar' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/libbcfs.so' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/plink' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/plink_driver' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/plink_reporter' --directory-prefix=/home/bcos_calc/bin"
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/bin/transpose_binary_matrix' --directory-prefix=/home/bcos_calc/bin"

cd /home/bcos_calc/data
su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/plink_test_job_for_centos_7.2' --directory-prefix=/home/bcos_calc/data"

su -l bcos_calc -c "wget --no-check-certificate 'https://download.bcplatforms.com/~bcos_src/mshackfest/scratchbox/run_plink.sh' --directory-prefix=/home/bcos_calc/jobdir"

chmod a=rwx /home/bcos_calc/bin/*
chmod a=rwx /home/bcos_calc/jobdir/*

cp /home/bcos_calc/bin/libbcfs.so /usr/lib/x86_64-linux-gnu/

if [ ! -d /usr/lib/x86_64-linux-gnu/libbcfs.so.0.1.0 ]
then
ln -s  /usr/lib/x86_64-linux-gnu/libbcfs.so.0.1.0 /usr/lib/x86_64-linux-gnu/libbcfs.so
fi

#task declaration to be done later in the Task creation
#su -l bcos_calc -c "/home/bcos_calc/jobdir/run_plink.sh"

exit 1