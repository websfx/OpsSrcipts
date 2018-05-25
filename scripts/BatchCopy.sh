#!/bin/sh

SERVER=(10.53.2.73 10.53.2.72 10.53.2.74 10.53.2.75)

function create_batch(){
	for BATCH_SERVER in ${SERVER[@]} ;do
		echo ${BATCH_SERVER}
		for BATCH_NAME in `cat batch_list_more.txt`;do
			BATCH_STATUS=$(ssh -p58422 Administrator@${BATCH_SERVER} "sc query ${BATCH_NAME} | grep -w STATE  | awk '{print \$4}'")
			if [ "${BATCH_STATUS}" != "Running" ];then
				ssh -p58422 Administrator@${BATCH_SERVER} "sc query ${BATCH_NAME}"
				echo ${BATCH_STATUS}
			else
				ssh -p58422 Administrator@${BATCH_SERVER} "sc query ${BATCH_NAME}"
				echo ${BATCH_STATUS}
			fi
		done
	done
}
create_batch

