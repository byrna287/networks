#!/usr/bin/env python3

# to run main.py server command is: python3 -m uvicorn main:app --reload

#convert decimal to binary
def decToBin(dec):
   b_num = ""
   while dec != 0:
      r = dec % 2
      b_num += str(r)
      dec = dec // 2
   while len(b_num) < 8:
      b_num += "0"
   return b_num[::-1]

#find class of an ip address from first number
#b_num = 8 digit binary number in string
def findClass(b_num):
   if b_num[0] == "0":
      return "A"
   elif b_num[:2] == "10":
      return "B"
   elif b_num[:3] == "110":
      return "C"
   elif b_num[:4] == "1110":
      return "D"
   elif b_num[:4] == "1111":
      return "E"

# find number of hosts and networks for each class
def netTable(ip_cls):
   nets_hosts_range = {
               "A": (128, 16777216, "0.0.0.0", "127.255.255.255"),
               "B": (16384, 65536, "128.0.0.0", "191.255.255.255"),
               "C": (2097152, 256, "192.0.0.0", "223.255.255.255"),
               "D": ("n/a", "n/a", "224.0.0.0", "239.255.255.255"),
               "E": ("n/a", "n/a", "240.0.0.0", "255.255.255.255")
               }
   return nets_hosts_range[ip_cls]

def binMaskLst(mask):
   mask_lst = mask.split(".")
   return [decToBin(int(n)) for n in mask_lst]   # turn subnet mask into binary

def numBits(b_mask_lst):
   return sum([len(b.replace("0", "")) for b in b_mask_lst])   # get rid of 0's, get sum of length of remaining 1's

def numSubnetsHosts(b_mask_lst, ip_cls):
   if ip_cls == "B":
      bits = numBits(b_mask_lst[2:])
      num_subnets = 2 ** bits
      num_addr_hosts = (2 ** (16-bits)) - 2
      return num_subnets, num_addr_hosts
   elif ip_cls == "C":
      bits = numBits(b_mask_lst[3])
      num_subnets = 2 ** bits
      num_addr_hosts = (2 ** (8-bits)) - 2
      return num_subnets, num_addr_hosts

def validSubnets(mask, ip_cls):
   if ip_cls == "B":
      mask_num = int(mask.split(".")[2])
   elif ip_cls == "C":
      mask_num = int(mask.split(".")[3])
   block = 256 - mask_num
   valid_addr_nums = []
   valid = 0
   while valid <= mask_num:
      valid_addr_nums.append(str(valid))
      valid += block
   return valid_addr_nums

def addrLst(ip, ip_cls, valid_addr_nums, type_addr=None):
   last_num_B = {"valid": "0", "bc": "1", "first": "254", "last": "255"}
   ip_lst = ip.split(".")
   valid = []
   lst_cpy = []
   for num in valid_addr_nums:
      if ip_cls == "B":
         lst_cpy = ip_lst[:2] + [num] + [last_num_B[type_addr]]
      elif ip_cls == "C":
         lst_cpy = ip_lst[:3] + [num]
      valid.append(".".join(lst_cpy))
   return valid

def classBValidAddr(ip, valid_addr_nums, type_addr):
   last_num_B = {"valid": "0", "bc": "1", "first": "254", "last": "255"}
   ip_lst = ip.split(".")
   valid = []
   lst_cpy = []
   for num in valid_addr_nums:
      lst_cpy = ip_lst[:2] + [num] + [last_num_B[type_addr]]
      valid.append(".".join(lst_cpy))
   return valid

def broadcastNums(block, valid_addr_nums):
   return [str(-1 + block + int(n)) for n in valid_addr_nums]

def firstNums(valid_addr_nums):
   return [str(1 + int(n)) for n in valid_addr_nums]

def lastNums(block, valid_addr_nums):
   return [str(-2 + block + int(n)) for n in valid_addr_nums]

def bitsNetworkMask(b_lst):
   b_str_lst = ["".join(b) for b in b_lst]
   counts = []
   for i in range(1, len(b_str_lst)):
      same_count = 0
      for j in range(len(b_str_lst[0])):
         if b_str_lst[0][j] == b_str_lst[i][j]:
            same_count += 1
         else:
            counts.append(same_count)
            break
   print(min(counts))

def networkMaskAddr(cidr_num):
   b_net_mask = []
   for i in range(4):
      if cidr_num >= 8:
         b_net_mask.append("1" * 8)
         cidr_num -= 8
      else:
         b_str = "1" * cidr_num
         while len(b_str) < 8:
            b_str += "0"
         b_net_mask.append(b_str)
         cidr_num = 0
   net_mask_addr = [str(binToDec(b_num)) for b_num in b_net_mask]
   return ".".join(net_mask_addr)

def nma2(cidr_num):
   ones = cidr_num
   zeros = 32 - cidr_num
   b_str = "1" * ones + "0" * zeros
   b_lst = []
   for i in range(0, len(b_str), 8):
      b_lst.append(b_str[i:i + 8])
   net_mask_addr = [str(binToDec(b_num)) for b_num in b_lst]
   return ".".join(net_mask_addr)

def binToDec(b_num):
   b_num = b_num[::-1]
   dec = 0
   for i in range(len(b_num)):
      dec += int(b_num[i]) * (2 ** i)
   return dec

if __name__ == '__main__':
   ip = "136.168.0.0"
   first = int(ip.split(".")[0])
   b_num = decToBin(first)
   ip_cls = findClass(b_num)

   #print("C", numSubnetsHosts(["11111111", "11111111", "11111111", "11000000"], "C"))
   #print("B", numSubnetsHosts(["11111111", "11111111", "11000000", "00000000"], "B"))
   #print("C", validSubnets("255.255.255.192", "C"))
   #print(classCValidAddr("192.168.10.0", ['0', '64', '128', '192']))
   #print("B", validSubnets("255.255.192.0", "B"))
   #print(classBValidAddr("172.16.0.0", ['0', '64', '128', '192'], "valid"))
   
   #print(broadcastNums(64, ['0', '64', '128', '192']))
   #print(['0', '64', '128', '192'])
   #print(firstNums(['0', '64', '128', '192']))
   #print(lastNums(64, ['0', '64', '128', '192']))
   #b_lst = [["11001101", "01100100","00000000","00000000"],["11001101","01100100","00000001","00000000"],["11001101","01100100","00000010","00000000"],["11001101","01100100","00000011","00000000"]]
   #b_lst = ["abcdef", "ahijkl", "anoaqr", "vtuvwx"]
   #print(bitsNetworkMask(b_lst))

   print(networkMaskAddr(22))
   print(nma2(22))
   #print(binToDec("1010"))
   print(numBits("192.4.16.0"))

   ["192.4.16.0", "192.4.17.0", "192.4.18.0","192.4.19.0","192.4.20.0","192.4.21.0","192.4.22.0","192.4.23.0","192.4.24.0","192.4.25.0","192.4.26.0","192.4.27.0","192.4.28.0","192.4.29.0","192.4.30.0","192.4.31.0"]
   print(networkMaskAddr(20))
