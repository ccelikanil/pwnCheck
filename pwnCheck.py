#!/usr/bin/python3

import requests, sys, time, json

headers = {
	'User-Agent': 'some_user_agent',
	'Accept': 'accept_these',
	'Accept-Language': 'language',
	'Cookie': 'cookie_monster'
}

result = []

with open(sys.argv[1], 'r') as inputFile:
	print("[!] File is being read...")
	print("[!] Performing requests...\n")
	
	ct = 0
	
	for line in inputFile:
		URL = 'https://haveibeenpwned.com/unifiedsearch/' # request URL
		URL += line # append mail to the URL
		r = requests.get(URL.strip(), headers=headers) # request object
		time.sleep(2) # prevent getting kicked out because of the rate limit
		
		if r.status_code == 200: # if status code is 200, it means mail is leaked 
			print("[+] Found: ", line)
			result.append(line)
			json_object = json.loads(r.text)				# json lengthini alıp bütün verideki name değerlerini çekmeye çalış
			var = len(json_object)
			
			for i in json_object.keys()[-1]:
				print(json_object['Breaches'][i]['Name'])
		
		elif r.status_code == 429:
			print("[!] Seems like you get kicked out because of the rate limit :/")
	
		else:
			print("[-] Not Found: ", line)
		
		ct += 1

with open(sys.argv[2], 'w') as outputFile:
	print("[!] Writing mails into", sys.argv[2] ,"...\n")
	for item in result:
		outputFile.write("".join(item) + "\n") # add mails to the output file
	
	print("[!] Total number of mails:", ct)
	print("[!] Total number of leaked mails:", len(result))	
	print("\n[!] DONE!")
