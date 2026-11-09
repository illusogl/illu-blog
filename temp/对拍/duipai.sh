#!/bin/bash
# 对拍主脚本：自动编译三件套，循环跑到 WA 为止
# 用法: bash duipai.sh
g++ -O2 sol.cpp -o sol && g++ -O2 bf.cpp -o bf && g++ -O2 gen.cpp -o gen || exit 1
for ((i = 1;; i++)); do
    ./gen $i > in.txt
    ./sol < in.txt > out1.txt
    ./bf < in.txt > out2.txt
    if ! diff -q out1.txt out2.txt > /dev/null; then
        echo "WA! seed=$i  (复现: ./gen $i > in.txt)"
        cat in.txt
        break
    fi
done
