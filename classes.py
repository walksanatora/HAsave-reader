import logging
from values import *

class HASave:
	data: bytearray
	save_version: int = 0
	section_count: int = 1
	values:dict = {}
	def __init__(self,data: bytearray):
		self.data = data
		self.save_version = self.data.pop(0)
		self.section_count = self.__ext_short__()
		while 1==1:
			try:
				key, l = self.__ext_str__()
			except IndexError:
				break
			if l == 0: continue
			logging.debug(f"read key: {key}, len: {l}")
			var_type = resolve_type(key)
			var = None
			logging.debug(f"type: {var_type}")
			if var_type == "short":var = self.__ext_short__()
			if var_type == "long":var  = self.__ext_long__()
			if var_type == "str":var = self.__ext_str__()
			if var == None:raise KeyError(f"INVALID KEY: {key}")
			logging.debug(f"value: {var}")
			self.values[key] = var
			print(self.data)

	def __ext_short__(self)->int:
		low = f"{self.data.pop(0):b}"
		high = f"{self.data.pop(0):b}"
		val = int(high+low,2)
		if val >= 32768: val -= 65536
		return val
	def __ext_long__(self)->int:
		lowest = f"{self.data.pop(0):b}"
		low = f"{self.data.pop(0):b}"
		high = f"{self.data.pop(0):b}"
		highest = f"{self.data.pop(0):b}"
		val = int(highest+high+low+lowest,2)
		if val >= 2147483648: val -= 4294967296
		return val
	def __ext_str__(self)->str:
		str_len = self.data.pop(0)
		string = ""
		for _ in range(str_len):
			val = self.data.pop(0)
			if val == 0: continue
			string += chr(val)
		return string,str_len
	def __repr__(self):
		return f"<HAsave v:{self.save_version} obj#: {len(self.values)}>"
	def __getitem__(self, key):
		return self.values[key]

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	logging.info("testing save_data/the_inventory")
	with open("save_data/the_inventory","rb") as save:
		ba = bytearray(save.read())
		save = HASave(ba)
		print(save)