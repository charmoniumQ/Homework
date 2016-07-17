#!/usr/bin/fish

echo "Compiling:"

if g++ -lm -lcrypt -O2 -pipe -DONLINE_JUDGE main2.cpp
   echo "Running:"
   #./a.out
   ./a.out < MainTest.txt > MainTestOut2.txt
end
