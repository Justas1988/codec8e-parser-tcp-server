import socket

HOST = socket.gethostbyname(socket.gethostname())  
PORT = 7494  #change this to your port

def input_trigger():
	print("Paste Codec 8E packet to parse it or:")
	print("Type SERVER to start the server or:")
	print("Type EXIT to stop the program")
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
		except Exception as e:
			print(f"error occured: {e} enter proper Codec8E packet or EXIT!!!")
			input_trigger()		

def codec_8e_checker(unchecked_packet):
	if str(unchecked_packet[16:16+2]).upper() != "8E":	
		print()	
		print(f"Invalid packet!!!!!!!!!!!!!!!!!!!")		
		return False
	else:
		try:
			checked_packet = unchecked_packet
			return codec_8e_parser(checked_packet)

		except Exception as e:
			print(f"Error occured: {e} enter proper Codec8E packet or EXIT!!!")
			input_trigger()

def start_server_tigger():
	print("server unfinished and does almost nothing")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	    s.bind((HOST, PORT))
	    while True:
	            s.listen()
	            print(f"listening port {PORT}")
	            conn, addr = s.accept()	 
	            conn.settimeout(10)           
	            with conn:
	                print(f"Connected by {addr}")
	                while True:
	                	try:
		                    data = conn.recv(1280)	                    
		                    print(f"data received = {data.hex()}")
		                    record_number = codec_8e_checker(data.hex())
		                    print(f"received records {record_number}")	
		                    print()                 
		                    if not data or record_number == False:
		                        break                    
		                    record_response = (record_number).to_bytes(4, byteorder='big')     
		                    conn.sendall(record_response)
		                    print(f"sent data = {record_response}")
		                except socket.timeout:
		                	print(f"Socket timed out. Closing connection with {addr}")
		                	break
                        	

def codec_8e_parser(codec_8E_packet): #think a lot before modifying  this function

	print (str("codec 8 string entered - " + codec_8E_packet))

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
		print()
		print (f"data from record {record_number}")	
		print (f"########################################")
		timestamp = avl_data_start[data_field_position:data_field_position+16]
		print (f"timestamp = {timestamp}")	
		data_field_position += len(timestamp)

		priority = avl_data_start[data_field_position:data_field_position+2]
		print (f"record priority = {priority}")

		data_field_position += len(priority)

		longtitude = avl_data_start[data_field_position:data_field_position+8]
		print (f"longtitude = {longtitude}")
		data_field_position += len(longtitude)

		latitude = avl_data_start[data_field_position:data_field_position+8]
		print (f"latitude = {latitude}")
		data_field_position += len(latitude)

		altitude = avl_data_start[data_field_position:data_field_position+4]
		print(f"altitude = {altitude}")
		data_field_position += len(altitude)

		angle = avl_data_start[data_field_position:data_field_position+4]
		print(f"angle = {angle}")
		data_field_position += len(angle)

		satelites = avl_data_start[data_field_position:data_field_position+2]
		print(f"satelites = {satelites}")
		data_field_position += len(satelites)

		speed = avl_data_start[data_field_position:data_field_position+4]
		print(f"speed = {speed}")
		data_field_position += len(speed)

		even_io_id = avl_data_start[data_field_position:data_field_position+4]
		print(f"event ID = {int(even_io_id, 16)}")
		data_field_position += len(even_io_id)

		total_io_elements = avl_data_start[data_field_position:data_field_position+4]
		total_io_elements_parsed = int(total_io_elements, 16)
		print(f"total I/O elements in record {record_number} = {total_io_elements_parsed}")
		data_field_position += len(total_io_elements)

		byte1_io_number = avl_data_start[data_field_position:data_field_position+4]
		byte1_io_number_parsed = int(byte1_io_number, 16)
		print(f"1 byte io count = {byte1_io_number_parsed}")
		data_field_position += len(byte1_io_number)
		io_dict = {}

		if byte1_io_number_parsed > 0:
			i = 1				
			while i <= byte1_io_number_parsed:
				key = avl_data_start[data_field_position:data_field_position+4]
				data_field_position += len(key)

				value = avl_data_start[data_field_position:data_field_position+2]
				io_dict[key] = value
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
				io_dict[key] = value
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
				io_dict[key] = value
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
				io_dict[key] = value
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
				io_dict[key] = value		
				data_field_position += len(value)
				print(f"avl_ID: {int(key, 16)} : {value}")
				print (f"data field postition = {data_field_position}")
				print (f"data_field_length = {2*data_field_length}")
				i += 1
		else:
			pass

		record_number += 1

	total_records_parsed = avl_data_start[data_field_position:data_field_position+2]
	print(f"total parsed records = {total_records_parsed}")
	print()
	return int(number_of_records)


input_trigger()