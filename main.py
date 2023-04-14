import socket
import json
import os
import datetime
import struct

HOST = socket.gethostbyname(socket.gethostname())  
PORT = 7494  #change this to your port

def input_trigger(): #triggers user input
	print("Paste Codec 8E packet to parse it or:")
	print("Type SERVER to start the server or:")
	print("Type EXIT to stop the program")
	device_imei = "default_IMEI"
	user_input = input("waiting for input: ")
	if user_input.upper() == "EXIT":
		print(f"exiting program............")
		exit()	

	elif user_input.upper() == "SERVER":
		start_server_tigger()
	else:		
		try:
			if codec_8e_checker(user_input) == False:
				print("Wrong input or invalid Codec8E packet")
				print()
				input_trigger()
			else:
				codec_parser_trigger(user_input, device_imei)
		except Exception as e:
			print(f"error occured: {e} enter proper Codec8E packet or EXIT!!!")
			input_trigger()		

def codec_8e_checker(codec8_packet): #does some basic check if codec is 8E, and passes it to parse function (checks must be improved later)
	if str(codec8_packet[16:16+2]).upper() != "8E":	
		print()	
		print(f"Invalid packet!!!!!!!!!!!!!!!!!!!")		
		return False
	else:
		return True

def codec_parser_trigger(codec8_packet, device_imei):
		try:			
			return codec_8e_parser(codec8_packet, device_imei)

		except Exception as e:
			print(f"Error occured: {e} enter proper Codec8E packet or EXIT!!!")
			input_trigger()

def imei_checker(hex_imei): #IMEI checker function
	imei_length = int(hex_imei[:4], 16)
#	print(f"IMEI length = {imei_length}")
	if imei_length != len(hex_imei[4:]) / 2:
		print(f"Not an IMEI - length is not correct!")
		return False
	else:
		pass

	ascii_imei = ascii_imei_converter(hex_imei)
	print(f"IMEI received = {ascii_imei}")
	if not ascii_imei.isnumeric() or len(ascii_imei) != 15:
		print(f"Not an IMEI - is not numeric!")
		return False
	else:
		return True

def ascii_imei_converter(hex_imei):
	return bytes.fromhex(hex_imei[4:]).decode()

def start_server_tigger(): #triggers server
	print("Starting server!")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	    s.bind((HOST, PORT))
	    while True:
	            s.listen()
	            print(f"// {time_stamper()} // listening port {PORT}")	           
	            conn, addr = s.accept()	 
	            conn.settimeout(20)           
	            with conn:
	                print(f"// {time_stamper()} // Connected by {addr}")	               
	               	device_imei = "default_IMEI"
	                while True:
	                	try:
		                    data = conn.recv(1280)	                    
		                    print(f"// {time_stamper()} // data received = {data.hex()}")		                   
		                    if not data:
		                    	break
		                    elif imei_checker(data.hex()) != False:
		                    	device_imei = ascii_imei_converter(data.hex())
		                    	imei_reply = (1).to_bytes(1, byteorder="big")
		                    	conn.sendall(imei_reply)
		                    	print(device_imei)
		                    	print (f"-- {time_stamper()} sending reply = {imei_reply}")		                    	
		                    elif codec_8e_checker(data.hex()) != False:
		                    	record_number = codec_parser_trigger(data.hex(), device_imei)
		                    	print(f"received records {record_number}")
		                    	print(f"from device IMEI = {device_imei}")	
		                    	print()  
		                    	record_response = (record_number).to_bytes(4, byteorder="big")     
		                    	conn.sendall(record_response)
		                    	print(f"// {time_stamper()} // response sent = {record_response.hex()}") 		                    	
		                    else:
		                    	print(f"// {time_stamper()} // no expected DATA received - dropping connection")		                    	
		                    	break                        
		             
		                except socket.timeout:
		                	print(f"// {time_stamper()} // Socket timed out. Closing connection with {addr}")
		                	break
                        	

def codec_8e_parser(codec_8E_packet, device_imei): #think a lot before modifying  this function
	print()
#	print (str("codec 8 string entered - " + codec_8E_packet))

	zero_bytes = codec_8E_packet[:8]
	print()
	print (str("zero bytes = " + zero_bytes))

	data_field_length = int(codec_8E_packet[8:8+8], 16)
	print (f"data field lenght = {data_field_length} bytes")
	codec_type = str(codec_8E_packet[16:16+2])
	print (f"codec type = {codec_type}")

	number_of_records = int(codec_8E_packet[18:18+2], 16)
	print (f"number of records = {number_of_records}")

	record_number = 1
	avl_data_start = codec_8E_packet[20:]
	data_field_position = 0
	while data_field_position < (2*data_field_length-6):		
		io_dict = {}
		io_dict["deviceIMEI"] = device_imei
		io_dict["server_time"] = time_stamper()
		print()
		print (f"data from record {record_number}")	
		print (f"########################################")
		timestamp = avl_data_start[data_field_position:data_field_position+16]
		io_dict["_timestamp_"] = device_time_stamper(timestamp)
		print (f"timestamp = {device_time_stamper(timestamp)}")	
		data_field_position += len(timestamp)

		priority = avl_data_start[data_field_position:data_field_position+2]
		io_dict["priority"] = int(priority, 16)
		print (f"record priority = {int(priority, 16)}")

		data_field_position += len(priority)

		longtitude = avl_data_start[data_field_position:data_field_position+8]
		io_dict["longtitude"] = struct.unpack('>i', bytes.fromhex(longtitude))[0]
		print (f"longtitude = {struct.unpack('>i', bytes.fromhex(longtitude))[0]}")
		data_field_position += len(longtitude)

		latitude = avl_data_start[data_field_position:data_field_position+8]
		print (f"latitude = {struct.unpack('>i', bytes.fromhex(latitude))[0]}")
		io_dict["latitude"] = struct.unpack('>i', bytes.fromhex(latitude))[0]
		data_field_position += len(latitude)

		altitude = avl_data_start[data_field_position:data_field_position+4]
		print(f"altitude = {int(altitude, 16)}")
		io_dict["altitude"] = int(altitude, 16)
		data_field_position += len(altitude)

		angle = avl_data_start[data_field_position:data_field_position+4]
		print(f"angle = {int(angle, 16)}")
		io_dict["angle"] = int(angle, 16)
		data_field_position += len(angle)

		satelites = avl_data_start[data_field_position:data_field_position+2]
		print(f"satelites = {int(satelites, 16)}")
		io_dict["satelites"] = int(satelites, 16)
		data_field_position += len(satelites)

		speed = avl_data_start[data_field_position:data_field_position+4]
		io_dict["speed"] = int(speed, 16)
		print(f"speed = {int(speed, 16)}")
		data_field_position += len(speed)

		event_io_id = avl_data_start[data_field_position:data_field_position+4]
		io_dict["eventID"] = event_io_id		
		print(f"event ID = {int(event_io_id, 16)}")
		data_field_position += len(event_io_id)

		total_io_elements = avl_data_start[data_field_position:data_field_position+4]
		total_io_elements_parsed = int(total_io_elements, 16)
		print(f"total I/O elements in record {record_number} = {total_io_elements_parsed}")
		data_field_position += len(total_io_elements)

		byte1_io_number = avl_data_start[data_field_position:data_field_position+4]
		byte1_io_number_parsed = int(byte1_io_number, 16)
		print(f"1 byte io count = {byte1_io_number_parsed}")
		data_field_position += len(byte1_io_number)
		

		if byte1_io_number_parsed > 0:
			i = 1				
			while i <= byte1_io_number_parsed:
				key = avl_data_start[data_field_position:data_field_position+4]
				data_field_position += len(key)

				value = avl_data_start[data_field_position:data_field_position+2]
				io_dict[int(key, 16)] = value
				data_field_position += len(value)
				print (f"avl_ID: {int(key, 16)} : {value}")
				i += 1
		else:
			pass

		byte2_io_number = avl_data_start[data_field_position:data_field_position+4]
		byte2_io_number_parsed = int(byte2_io_number, 16)
		print(f"2 byte io count = {byte2_io_number_parsed}")
		data_field_position += len(byte2_io_number)

		if byte2_io_number_parsed > 0:
			i = 1
			while i <= byte2_io_number_parsed:
				key = avl_data_start[data_field_position:data_field_position+4]
				data_field_position += len(key)

				value = avl_data_start[data_field_position:data_field_position+4]
				io_dict[int(key, 16)] = value
				data_field_position += len(value)
				print (f"avl_ID: {int(key, 16)} : {value}")
				i += 1
		else:
			pass

		byte4_io_number = avl_data_start[data_field_position:data_field_position+4]
		byte4_io_number_parsed = int(byte4_io_number, 16)
		print(f"4 byte io count = {byte4_io_number_parsed}")
		data_field_position += len(byte4_io_number)

		if byte4_io_number_parsed > 0:
			i = 1
			while i <= byte4_io_number_parsed:
				key = avl_data_start[data_field_position:data_field_position+4]
				data_field_position += len(key)

				value = avl_data_start[data_field_position:data_field_position+8]
				io_dict[int(key, 16)] = value
				data_field_position += len(value)
				print(f"avl_ID: {int(key, 16)} : {value}")
				i += 1
		else:
			pass

		byte8_io_number = avl_data_start[data_field_position:data_field_position+4]
		byte8_io_number_parsed = int(byte8_io_number, 16)
		print(f"8 byte io count = {byte8_io_number_parsed}")
		data_field_position += len(byte8_io_number)

		if byte8_io_number_parsed > 0:
			i = 1
			while i <= byte8_io_number_parsed:
				key = avl_data_start[data_field_position:data_field_position+4]
				data_field_position += len(key)

				value = avl_data_start[data_field_position:data_field_position+16]
				io_dict[int(key, 16)] = value
				data_field_position += len(value)
				print(f"avl_ID: {int(key, 16)} : {value}")
				i += 1
		else:
			pass

		byteX_io_number = avl_data_start[data_field_position:data_field_position+4]
		byteX_io_number_parsed = int(byteX_io_number, 16)
		print(f"X byte io count = {byteX_io_number_parsed}")
		data_field_position += len(byteX_io_number)

		if byteX_io_number_parsed > 0:
			i = 1
			while i <= byteX_io_number_parsed:
				key = avl_data_start[data_field_position:data_field_position+4]
				data_field_position += len(key)

				value_length = avl_data_start[data_field_position:data_field_position+4]
				data_field_position += 4
				value = avl_data_start[data_field_position:data_field_position+(2*(int(value_length, 16)))]
				io_dict[int(key, 16)] = value		
				data_field_position += len(value)
				print(f"avl_ID: {int(key, 16)} : {value}")
			#	print (f"data field postition = {data_field_position}")
			#	print (f"data_field_length = {2*data_field_length}")
				i += 1
		else:
			pass

		record_number += 1
		
		try: #writing dictionary to ./data/data.json
			json_printer(io_dict)
		except Exception as e:
			print(f"JSON writing error occured = {e}")

		print()
		print(io_dict)

	total_records_parsed = int(avl_data_start[data_field_position:data_field_position+2], 16)
	print()
	print(f"total parsed records = {total_records_parsed}")
	print()
	return int(number_of_records)

def json_printer(io_dict): #function to write JSON file with data
	json_data = json.dumps(io_dict, indent=4)
	data_path = "./data"
	json_file = "data.json"

	if not os.path.exists(data_path):
		os.makedirs(data_path)
	else:
		pass

	if not os.path.exists(os.path.join(data_path, json_file)):
		with open(os.path.join(data_path, json_file), "w") as file:
			file.write(json_data)
	else:
		with open(os.path.join(data_path, json_file), "a") as file:
			file.write(json_data)
	return

def time_stamper():
	current_server_time = datetime.datetime.now()
	server_time_stamp = current_server_time.strftime("%H:%M:%S %d-%m-%Y")
	return server_time_stamp

def device_time_stamper(timestamp):
	timestamp_ms = int(timestamp, 16) / 1000
	timestamp_utc = datetime.datetime.utcfromtimestamp(timestamp_ms)
	utc_offset = datetime.datetime.fromtimestamp(timestamp_ms) - datetime.datetime.utcfromtimestamp(timestamp_ms)
	timestamp_local = timestamp_utc + utc_offset
	formatted_timestamp_local = timestamp_local.strftime("%H:%M:%S %d-%m-%Y")
	formatted_timestamp_utc = timestamp_utc.strftime("%H:%M:%S %d-%m-%Y")
	formatted_timestamp = f"{formatted_timestamp_local} (local) / {formatted_timestamp_utc} (utc)"

	return formatted_timestamp

input_trigger()