#!/usr/bin/env python3

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

api_desc = """ 
   ### Ailbhe Byrne

   This is a webservice using FastAPI that includes 3 endpoints, which send and and receive JSON data.

   The 3 endpoints consist of an IP calculator, a subnet calculator and a supernet calculator.

"""

ipcalc_desc = """
   This endpoint takes in JSON data from a post request. The data contains an IP address in decimal dot notation, (i.e. 0.0.0.0).
   It returns information about the IP address consisting of: the class, the number of networks, the number of hosts, the first IP address and
   the last IP address.
"""

subnet_desc = """
   This endpoint takes in JSON data from a post request. The data contains a class B or class C IP address and a subnet mask, both in decimal
   dot notation. A subnet is when a network is divided into more networks and a subnet mask is used to identify the network and host parts of an address.  

   The endpoint will return information about the IP address
   and the subnet consisting of: the IP address in CIDR notation, the number of subnets, the number of addressable hosts, the valid subnets,
   the broadcast address and the valid hosts.
"""

supernet_desc = """
   This endpoint takes in JSON data from a post request. The data contains a list of class C IP addresses which are going to make up a supernet. 
   A supernet is made by combining networks into a larger network.

   It will return information about the supernet consisting of: the network in CIDR notation and the network mask.
"""

tags_metadata = [
   {
   "name": "IP Calculator",
   "description": ipcalc_desc,
   },
   {
   "name": "Subnet Calculator",
   "description": subnet_desc,
   },
   {
   "name": "Supernet Calculator",
   "description": supernet_desc,
   }
]

class Address(BaseModel):
   address: Optional[str] = None
   mask: Optional[str] = None
   addresses: Optional[list] = None

app = FastAPI(
   title="CA304 Networks 2 Assignment 1",
   description=api_desc,
   openapi_tags=tags_metadata,
)

ipcalc_desc2 = """
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "address": "string"  
   }  

   The string for address should be an IP address in decimal dot notation.

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "class": "string",  
   &nbsp;&nbsp; "num_networks": integer,  
   &nbsp;&nbsp; "num_hosts": integer,  
   &nbsp;&nbsp; "first_address": "string",  
   &nbsp;&nbsp; "last_address": "string"  
   }  

   The string for class will be a letter representing the class of the received IP address, i.e. A. (Depends on the binary of the first number of the IP address)  
   
   The integer for num_networks will be the number of networks that class has. (2 ^ network bits)  
   
   The integer for num_hosts will be the number of hosts that class has. (2 ^ host bits)  
   
   The string for first_address will be the first IP address of that class.  
   
   The string for last_address will be the last IP address of that class.  

   **Example input:**  
   {  
   &nbsp;&nbsp; "address":"192.168.10.0"  
   }  

   **Example output:**  
   {  
   &nbsp;&nbsp; "class":"C",  
   &nbsp;&nbsp; "num_networks":2097152,  
   &nbsp;&nbsp; "num_hosts":256,  
   &nbsp;&nbsp; "first_address":"192.0.0.0",  
   &nbsp;&nbsp; "last_address":"223.255.255.255"  
   }
"""

# IP Calculator
@app.post("/ipcalc/", tags=["IP Calculator"], description=ipcalc_desc2)
async def ip_info(address: Address):
   addr_dict = address.dict()
   ip = addr_dict["address"]
   ip_first_dec = int(ip.split(".")[0])

   ip_cls = findClass(ip_first_dec)             # get class of ip address
   nets, hosts, first, last = netTable(ip_cls)  # get class information from table
   return {
            "class": ip_cls,
            "num_networks": nets,
            "num_hosts": hosts,
            "first_address": first,
            "last_address": last
          }

# dictionary of information about the classes
def netTable(ip_cls):
   nets_hosts_range = {
                        "A": (128, 16777216, "0.0.0.0", "127.255.255.255"),
                        "B": (16384, 65536, "128.0.0.0", "191.255.255.255"),
                        "C": (2097152, 256, "192.0.0.0", "223.255.255.255"),
                        "D": ("N/A", "N/A", "224.0.0.0", "239.255.255.255"),
                        "E": ("N/A", "N/A", "240.0.0.0", "255.255.255.255")
                      }
   return nets_hosts_range[ip_cls]

# get class of ip address (takes first number of ip address)
def findClass(dec):
   b_num = decToBin(dec)   # get number in binary
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

# change decimal number to binary (string)
def decToBin(dec):
   b_num = ""
   while dec != 0:
      r = dec % 2
      b_num += str(r)
      dec = dec // 2
   while len(b_num) < 8:
      b_num += "0"
   return b_num[::-1]

subnet_desc2 = """
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "address": "string",  
   &nbsp;&nbsp; "mask": "string"  
   }  

   The string for address should be an IP address in decimal dot notation.  
   
   The string for mask should be an IP address in decimal dot notation.

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "address_cidr": "string",  
   &nbsp;&nbsp; "num_subnets": integer,  
   &nbsp;&nbsp; "addressable_hosts_per_subnet": integer,  
   &nbsp;&nbsp; "valid_subnets": list,  
   &nbsp;&nbsp; "broadcast_addresses": list,  
   &nbsp;&nbsp; "first_addresses": list,  
   &nbsp;&nbsp; "last_addresses": list  
   }  

   The string for address_cidr will be the IP address in CIDR notation. (address + "/" + number of bits in subnet mask)  
   
   The integer for num_subnets will be the amount of subnets the subnet mask produces. (2 ^ number of subnet bits)  
   
   The integer for addressable_hosts_per_subnet will be the amount of available hosts for the subnet, which excludes subnet address and broadcast address. ((2 ^ 
   number of unmasked bits) - 2)  
   
   The list for valid_subnets will be a list of IP addresses as strings. They go from ending in 0 or 0.0 and increase in the block size to the mask.  
   
   The list for broadcast_addresses will be a list of IP addresses as strings. They start below the 2nd subnet, increasing in the block size.  
   
   The list for first_addresses will be a list of IP addresses as strings. They start above the 1st subnet, increasing in the block size.  
   
   The list for last_addresses will be a list of IP addresses as strings. They start below the 1st broadcast address, increasing in the block size.  

   **Example input:**  
   {  
   &nbsp;&nbsp; "address": "172.16.0.0",  
   &nbsp;&nbsp; "mask": "255.255.192.0"  
   }  

   **Example output:**  
   {  
   &nbsp;&nbsp; "address_cidr":"172.16.0.0/18",  
   &nbsp;&nbsp; "num_subnets":4,  
   &nbsp;&nbsp; "addressable_hosts_per_subnet":16382,  
   &nbsp;&nbsp; "valid_subnets":["172.16.0.0","172.16.64.0","172.16.128.0","172.16.192.0"],  
   &nbsp;&nbsp; "broadcast_addresses":["172.16.63.255","172.16.127.255","172.16.191.255","172.16.255.255"],  
   &nbsp;&nbsp; "first_addresses":["172.16.0.1","172.16.64.1","172.16.128.1","172.16.192.1"],  
   &nbsp;&nbsp; "last_addresses":["172.16.63.254","172.16.127.254","172.16.191.254","172.16.255.254"]  
   }

"""

# Subnet Calculator
@app.post("/subnet/", tags=["Subnet Calculator"], description=subnet_desc2)
def subnet_info(address: Address):
   addr_dict = address.dict()
   ip = addr_dict["address"]
   ip_first_dec = int(ip.split(".")[0])
   ip_cls = findClass(ip_first_dec)   # get class of ip address

   mask = addr_dict["mask"]
   b_mask_lst = binLst(mask)          # change subnet mask to list of binary strings

   cidr_num = numBits(b_mask_lst)        # get number used for cidr notation (number of 1's in subnet mask)
   cidr_addr = ip + "/" + str(cidr_num)  # change ip address to cidr notation
   
   num_subnets, num_addr_hosts = numSubnetsHosts(b_mask_lst, ip_cls)   # get number of subnets and number of addressable hosts
   block, valid_addr_nums = validSubnets(mask, ip_cls)                 # get block number, list of numbers of valid subnets
   valid_subnets = addrLst(ip, ip_cls, valid_addr_nums, "valid")       # get list of valid subnet addresses
   broadcast_addr = addrLst(ip, ip_cls, broadcastNums(block, valid_addr_nums), "bc")   # get list of broadcast addresses
   first_addr = addrLst(ip, ip_cls, firstNums(ip_cls, valid_addr_nums), "first")       # get list of first addresses
   last_addr = addrLst(ip, ip_cls, lastNums(ip_cls, block, valid_addr_nums), "last")   # get list of last addresses
   return {
            "address_cidr": cidr_addr,
            "num_subnets": num_subnets,
            "addressable_hosts_per_subnet": num_addr_hosts,
            "valid_subnets": valid_subnets,
            "broadcast_addresses": broadcast_addr,
            "first_addresses": first_addr,
            "last_addresses": last_addr,
          }

# turn subnet mask into list of binary strings
def binLst(mask):
   mask_lst = mask.split(".")
   return [decToBin(int(n)) for n in mask_lst]

# get rid of 0's, get sum of length of remaining 1's, in list of binary strings
def numBits(b_mask_lst):
   return sum([len(b.replace("0", "")) for b in b_mask_lst])

# get number of subnets and number of addressable hosts from subnet mask as list of binary strings and ip class
def numSubnetsHosts(b_mask_lst, ip_cls):
   if ip_cls == "B":
      bits = numBits(b_mask_lst[2:])   # get number of 1's in last 16 binary digits
      num_subnets = 2 ** bits
      num_addr_hosts = (2 ** (16 - bits)) - 2  # 16 - bits = number of 0's in last 16 binary digits
      return num_subnets, num_addr_hosts
   elif ip_cls == "C":
      bits = numBits(b_mask_lst[3])    # get number of 1's in last 8 binary digits
      num_subnets = 2 ** bits
      num_addr_hosts = (2 ** (8 - bits)) - 2   # 8 - bits = number of 0's in last 8 binary digits
      return num_subnets, num_addr_hosts

# get valid subnet numbers from subnet mask and ip class, returns block and list of numbers as strings
def validSubnets(mask, ip_cls):
   if ip_cls == "B":
      mask_num = int(mask.split(".")[2])    # class B: subnet mask number is 3rd number
   elif ip_cls == "C":
      mask_num = int(mask.split(".")[3])    # class C: subnet mask number is last number
   block = 256 - mask_num                   # block size = amount between valid subnets
   valid_addr_nums = []
   valid = 0
   while valid <= mask_num:
      valid_addr_nums.append(str(valid))    # add string of valid subnet number to list
      valid += block
   return block, valid_addr_nums

# change ip address and list of numbers pertaining to certain types of addresses to a list of ip addresses as strings
def addrLst(ip, ip_cls, addr_nums, type_addr=None):
   last_num_B = {"valid": "0", "bc": "255", "first": "1", "last": "254"}   # dictionary for last number of class B addresses, depending on type of address
   ip_lst = ip.split(".")
   valid = []
   lst_cpy = []
   for num in addr_nums:
      if ip_cls == "B":
         lst_cpy = ip_lst[:2] + [num] + [last_num_B[type_addr]]   # class B: ip address = first 2 nums of ip + num from list + num for type of address
      elif ip_cls == "C":
         lst_cpy = ip_lst[:3] + [num]                             # class C: ip address = first 3 nums of ip + num from list
      valid.append(".".join(lst_cpy))                             # join list on . to make string for ip address
   return valid

# get list of numbers used for broadcast addresses for each subnet
def broadcastNums(block, valid_addr_nums):
   return [str(-1 + block + int(n)) for n in valid_addr_nums]   # valid subnet number + block - 1

# get list of numbers used for first addresses for each subnet
def firstNums(ip_cls, valid_addr_nums):
   if ip_cls == "B":
      return valid_addr_nums      # class B: same number as valid subnet (last number changes)
   elif ip_cls == "C":
      return [str(1 + int(n)) for n in valid_addr_nums]   # class C: next number after valid subnet

# get list of numbers used for last addresses for each subnet
def lastNums(ip_cls, block, valid_addr_nums):
   if ip_cls == "B":
      return broadcastNums(block, valid_addr_nums)        # class B: same number as broadcast address (last number changes)
   elif ip_cls == "C":
      return [str(-2 + block + int(n)) for n in valid_addr_nums]   # class C: number before broadcast address

supernet_desc2 = """
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "addresses": list,  
   }

   The list for addresses should be a list of contiguous class C IP addresses as strings.  

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "address": "string",  
   &nbsp;&nbsp; "mask": "string",  
   }  

   The string for address will be the network in CIDR notation. (first network IP address + "/" + number of network bits)  

   The string for mask will be the network mask. (binary number made from network bits + trailing 0's, changed into decimal dot notation)  

   **Example input:**  
   {  
    &nbsp;&nbsp; "addresses":["205.100.0.0","205.100.1.0","205.100.2.0","205.100.3.0"]  
   }  

   **Example output:**  
   {  
   &nbsp;&nbsp; "address":"205.100.0.0/22",  
   &nbsp;&nbsp; "mask":"255.255.252.0"  
   }
"""

# Supernet Calculator
@app.post("/supernet/", tags=["Supernet Calculator"], description=supernet_desc2)
def supernet_info(address: Address):
   addr_dict = address.dict()
   addr_lst = addr_dict["addresses"]
   b_lst = [binLst(addr) for addr in addr_lst]    # change addresses to lists of binary strings
   cidr_num = bitsNetworkMask(b_lst)              # get cidr number of network
   cidr_addr = addr_lst[0] + "/" + str(cidr_num)  # change address to cidr notation of network
   net_mask_addr = networkMaskAddr(cidr_num)      # get ip address of network mask
   return {
            "address": cidr_addr,
            "mask": net_mask_addr
          }

# get number of bits in network mask (common prefix of ip addresses in binary), from list of lists of binary strings
def bitsNetworkMask(b_lst):
   b_str_lst = ["".join(b) for b in b_lst]    # change list of lists to a list of strings
   counts = []
   for i in range(1, len(b_str_lst)):         # i to compare every binary string to first binary string
      same_count = 0
      for j in range(len(b_str_lst[0])):          # j to compare characters of strings
         if b_str_lst[0][j] == b_str_lst[i][j]:   # if characters match
            same_count += 1                       # count number of matching characters
         else:                             # if characters don't match
            counts.append(same_count)      # add count to list
            break                          # exit inner for loop
   return min(counts)        # smallest in list is earliest they didn't match (common prefix)

# get network mask address from cidr number of network mask
def networkMaskAddr(cidr_num):
   ones = cidr_num
   zeros = 32 - cidr_num     # an address is 32 bits long
   b_str = "1" * ones + "0" * zeros
   b_lst = []
   for i in range(0, len(b_str), 8):    # i increases in jumps of 8
      b_lst.append(b_str[i:i + 8])      # add binary numbers as strings of length 8
   net_mask_addr = [str(binToDec(b_num)) for b_num in b_lst]   # change binary numbers to decimal numbers (string)
   return ".".join(net_mask_addr)                              # join on . to make ip address

# change binary number to decimal
def binToDec(b_num):
   b_num = b_num[::-1]
   dec = 0
   for i in range(len(b_num)):
      dec += int(b_num[i]) * (2 ** i)
   return dec
