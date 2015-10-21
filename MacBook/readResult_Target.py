#!/usr/bin/python
import sys

print '**************************************'
print '         processing results'
print '**************************************'
print ''
bitLenExp = 10
bitNumExp = 10
opLen = 2
opNumExp = 10
opOrder = 0
opType = 0
opWrite = 1
mode = 'Target'
dir = '/home/shuangchenli/nvPIM/avx_test/resultTarget/'
r = open('proResult.txt','w')
for opLen in [2,4,8,16,32,64,128,256,512,1024]:
  print('processing opLen' + str(opLen) + '\n')
  for bitLenExp in range(10, 21):
    for bitNumExp in range(10,17):
      task = str(bitLenExp) + '-' + str(bitNumExp) + '-' + str(opLen) + '-' + str(opNumExp) + '-' + str(opOrder) + '-' + str(opType) + '-' + str(opWrite)
      f = open(dir + task + '.txt', 'r')
      for line in f:
        if line.find('dram') > -1:
          Rdram_power = line.split()[1]
          Rdram_energy = line.split()[3]
        if line.find('100.00%') > -1:
          Rpower = line.split()[1]
          Renergy = line.split()[3]
      f.close()
      f = open(dir + '/' + task + '/sim.out', 'r')
      for line in f:
        if line.find('Instructions') > -1:
          Rinstr = line.split()[2]
        if line.find('IPC') > -1:
          Ripc = line.split()[2]
        if line.find('Time') > -1:
          Rtime = line.split()[3]
        if line.find('num dram accesses') > -1:
          Rmem_access = line.split()[4]
        if line.find('dram access latency') > -1:
          Rmem_latency = line.split()[6]
        if line.find('dram bandwidth') > -1:
          Rmem_band = line.split()[5]
      f.close()
      #r.write(str(bitLenExp) + ', ' + str(bitNumExp) + ', ' + str(opLen) + ', ' + str(opNumExp) + ', ' + str(opOrder) + ', ' + str(opType) + ', ' + str(opWrite))
      #r.write(', ')
      r.write(Rtime)
      r.write(', ')
      r.write(Rinstr)
      r.write(', ')
      r.write(Ripc)
      r.write(', ')
      r.write(Rmem_access)
      r.write(', ')
      r.write(Rmem_latency)
      r.write(', ')
      r.write(Rmem_band)
      r.write(', ')
      r.write(Rpower)
      r.write(', ')
      r.write(Renergy)
      r.write(', ')
      r.write(Rdram_power)
      r.write(', ')
      r.write(Rdram_energy) 
      r.write('\n')
r.close()





      
