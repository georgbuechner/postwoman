#!/bin/bash

sed -i '2ipath_to_configs=$('$PWD'/configs)' postwoman.sh
cp postwoman.sh /usr/bin/postwoman.sh
mkdir results
