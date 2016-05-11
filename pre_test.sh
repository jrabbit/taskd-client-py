#!/bin/bash
docker run -it -p 9001:53589 -d --name taskc_test jrabbit/taskd
export TEST_UUID=`docker exec taskc_test taskd add user Public test_user | grep key | awk '{ print substr($0, 15)}'`