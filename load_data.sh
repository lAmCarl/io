#!/bin/bash
echo Copying files onto instance
while read -r file_name
	do
		until scp -o StrictHostKeyChecking=no -C -i opensesame.pem $file_name ubuntu@$1:~/.
		do
			sleep 0.1
		done
	done < files.txt
echo Done

ssh -i opensesame.pem ubuntu@$1 'bash -s' < install_pkgs.sh
