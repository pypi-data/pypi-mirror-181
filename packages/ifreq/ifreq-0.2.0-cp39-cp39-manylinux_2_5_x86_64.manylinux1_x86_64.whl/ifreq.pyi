
class ifreq:
	''' Control Network Interface In Object Oriented Method. '''

	def ifr_name (self, ifname: str = None) -> str:
		'''  'ifr_name' variable.\n
			Returns the 'ifr_name' value if ifname is None\n
			else 'ifr_name' is set to 'ifname'. '''

	ifr_ifindex: int

	def ifr_newname (self, newname: int) -> str:
		'''  'ifr_newname' variable.\n
			'ifr_newname' is set to 'newname'. '''

	ifr_flags : int

	def ifr_addr (self, if_addr: str = None) -> str:
		'''  'ifr_addr' variable.\n
			Returns the 'ifr_addr' value if 'if_addr' is None.\n
			else 'ifr_addr' is set to 'if_addr'.  '''
	def ifr_dstaddr (self, if_dstaddr: str = None) -> str:
		'''  'ifr_dstaddr' variable.\n
			Returns the 'ifr_dstaddr' value if 'if_dstaddr' is None.\n
			else 'ifr_dstaddr' is set to 'if_dstaddr'.  '''
	def ifr_broadaddr (self, if_broadaddr: str = None) -> str:
		'''  'ifr_broadaddr' variable.\n
			Returns the 'ifr_broadaddr' value if 'if_broadaddr' is None.\n
			else 'ifr_broadaddr' is set to 'if_broadaddr'.  '''
	def ifr_netmask (self, if_netmask: str = None) -> str:
		'''  'ifr_netmask' variable.\n
			Returns the 'ifr_netmask' value if 'if_netmask' is None.\n
			else 'ifr_netmask' is set to 'if_netmask'.  '''

	ifr_mtu: int
	ifr_keepalive: int # unsigned long
	ifr_qlen: int

	def ifr_hwaddr (self, if_hwaddr: str = None) -> str:
		'''  'ifr_hwaddr' variable.\n
			Returns the 'ifr_hwaddr' value if 'if_hwaddr' is None.\n
			else 'ifr_hwaddr' is set to 'if_hwaddr'.  '''


	def get_if_index (self, sock: int) -> int:
		'''  Get interface index from interface mapping according to 'ifr_name' value.
			On success, interface index is stored in 'ifr_ifindex' variable  and 0 is returned.
			On error, -1 is returned. '''
	def get_if_name (self, sock: int) -> int:
		'''  Get interface name according to 'ifr_ifindex' value.\n
			On success, interface name is stored in 'ifr_name' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_name (self, sock: int) -> int:
		'''  Set interface name according to 'ifr_newname' value for given interface 'ifr_name'.\n
			On success, interface name is changed according to 'ifr_newname' variable  and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_flags (self, sock: int) -> int:
		'''  Get interface flags according to 'ifr_name'.\n
			On success, flags is stored in 'ifr_flags' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_flags (self, sock: int) -> int:
		'''  Set interface flags according to 'ifr_flags' value for given interface 'ifr_name'.\n
			On success, interface flags is changed according to 'ifr_flags' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_addr (self, sock: int) -> int:
		'''  Get PA(Provider Aggregatable)/IP(Internet Protocol) address of given interface 'ifr_name'.\n
			On success, IP address is stored in 'ifr_addr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_addr (self, sock: int) -> int:
		'''  Set PA(Provider Aggregatable)/IP(Internet Protocol) address according to 'ifr_addr' value for given interface 'ifr_name'.\n
			On success, IP address is changed according to 'ifr_addr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_dstaddr (self, sock: int) -> int:
		'''  Get remote PA(Provider Aggregatable)/destination IP(Internet Protocol) address of given interface 'ifr_name'.\n
			On success, destination IP address is stored in 'ifr_dstaddr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_dstaddr (self, sock: int) -> int:
		'''  Set remote PA(Provider Aggregatable)/destination IP(Internet Protocol) address according to 'ifr_dstaddr' value for given interface 'ifr_name'.\n
			On success, IP address is changed according to 'ifr_dstaddr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_brdaddr (self, sock: int) -> int:
		'''  Get broadcast PA(Provider Aggregatable)/broadcast IP(Internet Protocol) address of given interface 'ifr_name'.\n
			On success, broadcast IP address is stored in 'ifr_broadaddr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_brdaddr (sock: int) -> int:
		'''  Set broadcast PA(Provider Aggregatable)/broadcast IP(Internet Protocol) address according to 'ifr_broadaddr' value for given interface 'ifr_name'.\n
			On success, broadcast IP address is changed according to 'ifr_broadaddr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_netmask (self, sock: int) -> int:
		'''  Get network PA(Provider Aggregatable) mask or network IP(Internet Protocol) mask of given interface 'ifr_name'.\n
			On success, network IP mask is stored in 'ifr_netmask' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_netmask (self, sock: int) -> int:
		'''  Set network PA(Provider Aggregatable) mask or network IP(Internet Protocol) mask according to 'ifr_netmask' value for given interface 'ifr_name'.\n
			On success, network IP mask is changed according to 'ifr_netmask' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_mtu (self, sock: int) -> int:
		'''  Get MTU(Maximum transmission unit) size of given interface 'ifr_name'.\n
			On success, MTU is stored in 'ifr_mtu' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_mtu (self, sock: int) -> int:
		'''  Set MTU(Maximum transmission unit) size according to 'ifr_mtu' value for given interface 'ifr_name'.\n
			On success, MTU is changed according to 'ifr_mtu' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_hwaddr (self, sock: int) -> int:
		'''  Get hardware address of given interface 'ifr_name'.\n
			On success, hardware address is stored in 'ifr_hwaddr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_hwaddr (self, sock: int) -> int:
		'''  Set hardware address according to 'ifr_hwaddr' value for given interface 'ifr_name'.\n
			On success, hardware address is changed according to 'ifr_hwaddr' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_keepalive (self, sock: int) -> int:
		'''  Get keepalive timeout of given interface 'ifr_name'.\n
			On success, keepalive timeout is stored in 'ifr_keepalive' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_keepalive (self, sock: int) -> int:
		'''  Set keepalive timeout in sec according to 'ifr_keepalive' value for given interface 'ifr_name'.\n
			On success, keepalive timeout is changed according to 'ifr_keepalive' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_outfill (self, sock: int) -> int:
		'''  Get outfill timeout of given interface 'ifr_name'.\n
			On success, outfill timeout is stored in 'ifr_outfill' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_outfill (self, sock int) -> int:
		'''  Set outfill timeout according to 'ifr_outfill' value for given interface 'ifr_name'.\n
			On success, outfill timeout is changed according to 'ifr_outfill' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def get_if_txqlen (self, sock: int) -> int:
		'''  Get the tx queue length of given interface 'ifr_name'.\n
			On success, the tx queue length is stored in 'ifr_qlen' variable and 0 is returned.\n
			On error, -1 is returned. '''
	def set_if_txqlen (self, sock: int) -> int:
		'''  Set the tx queue length according to 'ifr_qlen' value for given interface 'ifr_name'.
			On success, the tx queue length is changed according to 'ifr_qlen' variable and 0 is returned.
			On error, -1 is returned. */
