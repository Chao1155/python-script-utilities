#!/usr/bin/python
import sys

print '**************************************'
print '         generating scripts'
bitLenExp = 10
bitNumExp = 10
opLen = 2
opNumExp = 10
opOrder = 0
opType = 0
opWrite = 1
mode = 'Target'

for bitNumExp in range(10,17):
  opLen = 2
  while( opLen < 1025 ):
    task = mode + '-' + str(bitLenExp) + '_20-' + str(bitNumExp) + '-' + str(opLen) + '-' + str(opNumExp) + '-' + str(opOrder) + '-' + str(opType) + '-' + str(opWrite)
    f = open('./bashes/run_' + task + '.job', 'w')
    f.write('#!/bin/bash\n')
    f.write('\n')
    f.write('#' + task + '\n')
    f.write('\n')
    f.write('#PBS -l nodes=1:ppn=1 \n')
    f.write('#PBS -l walltime=20:00:00 \n')
    f.write('#PBS -M shuangchenli@ece.ucsb.edu\n')
    f.write('#PBS -m a\n')
    f.write('#PBS -j oe\n')
    f.write('#PBS -o /home/shuangchenli/nvPIM/avx_test/' + task + '.out\n')
    f.write('echo "Job started on `hostname` at `date`"\n')
    f.write('cd /home/shuangchenli/nvPIM/avx_test\n')
    f.write('\n')
    f.write('\n')
    f.write('bitNumExp=' + str(bitNumExp) + '\n')
    f.write('opLen=' + str(opLen) + '\n')
    f.write('opNumExp=' + str(opNumExp) + '\n')
    f.write('opOrder=' + str(opOrder) + '\n')
    f.write('opType=' + str(opType) + '\n')
    f.write('opWrite=' + str(opWrite) + '\n')
    f.write('model="Target"\n')
    f.write('workpath="/home/shuangchenli/nvPIM/avx_test/result'+mode+'/"\n')
    f.write('\n')
    f.write('for (( bitLenExp=' + str(bitLenExp) + '; bitLenExp<=20; bitLenExp++ ))\n')
    f.write('do\n')
    #f.write('  for (( bitNumExp=' + str(bitNumExp) + '; bitNumExp<=16; bitNumExp++ ))\n')
    #f.write('  do\n')
    f.write('      task=$bitLenExp-$bitNumExp-$opLen-$opNumExp-$opOrder-$opType-$opWrite\n')
    f.write('      echo "Processing "$mode"-"$task"..."\n')
    f.write('      rm -f -r $workpath$mode$task\n')
    f.write('      rm -f $workpath$mode$task".txt"\n')
    f.write('      mkdir $workpath$mode$task\n')
    f.write('      /home/shuangchenli/sniper/run-sniper -n 4 -d $workpath$mode$task"/" -c /home/shuangchenli/nvPIM/avx_test/haswell-i5.cfg -s markers:stats --power -- /home/shuangchenli/nvPIM/avx_test/avx $bitLenExp $bitNumExp $opLen $opNumExp $opOrder $opType $opWrite > $workpath$mode$task".txt"\n')
    f.write('      rm $workpath$mode$task"/sim.stats.sqlite3"\n')
    #f.write('  done\n')
    f.write('done\n')
    f.write('\n')
    f.write('echo " "\n')
    f.write('echo "Job Ended at `date`"\n')
    f.write('echo " "\n')
    f.write('\n')
    f.close();
    opLen = opLen*2

  
#for line in f:
#  if line.find('--') > -1:
#    counter = counter + 1;
#    if counter%1000000 == 0:
#      print 'processing ', str(counter)
#  if line.find('xchg %bx, %bx') > -1:
#    print 'Magic Found at ', str(counter)
print '**************************************'
