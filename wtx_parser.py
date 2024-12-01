from lxml import etree
import os

class WTXParser:
	def parse_file(self, file_path, file_type):
		"""
		Parse WTX file based on its type and return structured content
		"""
		if not os.path.exists(file_path):
			raise FileNotFoundError(f"File not found: {file_path}")
			
		file_extension = os.path.splitext(file_path)[1].lower()
		
		if file_type == "map":
			return self._parse_map(file_path)
		elif file_type == "system":
			return self._parse_system(file_path)
		elif file_type == "typetree":
			return self._parse_typetree(file_path)
		else:
			raise ValueError(f"Unsupported file type: {file_type}")
	
	def _parse_map(self, file_path):
		"""Parse WTX map file (.mmc)"""
		tree = etree.parse(file_path)
		root = tree.getroot()
		
		map_data = {
			'name': root.get('name', ''),
			'inputs': [],
			'outputs': [],
			'functions': [],
			'transformations': []
		}
		
		# Parse input cards
		for input_card in root.findall(".//InputCard"):
			map_data['inputs'].append({
				'name': input_card.get('name', ''),
				'type': input_card.get('type', ''),
				'format': input_card.get('format', '')
			})
			
		# Parse output cards
		for output_card in root.findall(".//OutputCard"):
			map_data['outputs'].append({
				'name': output_card.get('name', ''),
				'type': output_card.get('type', ''),
				'format': output_card.get('format', '')
			})
			
		# Parse functions and transformations
		for function in root.findall(".//Function"):
			map_data['functions'].append({
				'name': function.get('name', ''),
				'type': function.get('type', ''),
				'inputs': [input.get('ref') for input in function.findall('Input')],
				'outputs': [output.get('ref') for output in function.findall('Output')]
			})
			
		return map_data
	
	def _parse_system(self, file_path):
		"""Parse WTX system file (.sys)"""
		tree = etree.parse(file_path)
		root = tree.getroot()
		
		system_data = {
			'name': root.get('name', ''),
			'components': [],
			'connections': []
		}
		
		# Parse components
		for component in root.findall(".//Component"):
			system_data['components'].append({
				'name': component.get('name', ''),
				'type': component.get('type', ''),
				'properties': {prop.get('name'): prop.get('value') 
							 for prop in component.findall('Property')}
			})
			
		# Parse connections
		for connection in root.findall(".//Connection"):
			system_data['connections'].append({
				'from': connection.get('from', ''),
				'to': connection.get('to', ''),
				'type': connection.get('type', '')
			})
			
		return system_data
	
	def _parse_typetree(self, file_path):
		"""Parse WTX type tree file (.tts)"""
		tree = etree.parse(file_path)
		root = tree.getroot()
		
		type_data = {
			'name': root.get('name', ''),
			'types': []
		}
		
		def parse_type(type_elem):
			type_info = {
				'name': type_elem.get('name', ''),
				'datatype': type_elem.get('datatype', ''),
				'children': []
			}
			
			for child in type_elem.findall('./Type'):
				type_info['children'].append(parse_type(child))
				
			return type_info
		
		# Parse all top-level types
		for type_elem in root.findall('./Type'):
			type_data['types'].append(parse_type(type_elem))
			
		return type_data