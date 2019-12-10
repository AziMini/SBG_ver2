#!/bin/bash

if (($# < 1)); then
	echo "$0 [Audio File]"
else
	while ((1)); do
		mpg123 -q $1
	done
fi
