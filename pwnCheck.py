#!/usr/bin/python3

import requests, sys, time, json

headers = {
	'User-Agent': 'agent_smith',
	'Accept': 'accept_em_all',
	'Accept-Language': 'language',
	'Cookie': 'cookie_monster'
}

result = []
leak = []

with open(sys.argv[1], 'r') as inputFile:
	print("[!] File is being read...")
	print("[!] Performing requests...\n")
	
	ct = 0
	
	for line in inputFile:
		URL = 'https://haveibeenpwned.com/unifiedsearch/' # request URL
		URL += line # append mail to the URL
		r = requests.get(URL.strip(), headers=headers) # request object
		time.sleep(2) # prevent getting kicked out because of the rate limit
		
		i = 0
		leakct = 0
		
		if r.status_code == 200: # if status code is 200, it means mail is leaked 
			print("[+] Found: ", line)
			result.append(line)
			
			json_object = json.loads(r.text)
			
			while (len(json_object) < i or json_object['Breaches'][i]['Name'] != None):
				print("Leak", i+1, ":", json_object['Breaches'][i]['Name'], "- Breach Date:", json_object['Breaches'][i]['BreachDate'])
				
				leak.append(json_object['Breaches'][i]['Name'])
				leak.append(json_object['Breaches'][i]['BreachDate'])
				
				i+=1
				leakct+=1

				if(len(json_object) < i or json_object['Breaches'][i]['Name'] == None): # check whether the index number is out of range or index is null
					i = 0
					leakct = 0
					print("-----------------------\n")
					break
			
		elif r.status_code == 429:
			print("[!] Seems like you got kicked out because of the rate limit :/")
	
		else:
			print("[-] Not Found: ", line)
			print("-----------------------\n")
		
		ct+=1

with open(sys.argv[2], 'w') as outputFile:
	x = 0
	
	print("[!] Writing information into", sys.argv[2] ,"...\n")
	
	for item in result:
		outputFile.write("".join(item) + "\n") # add mails to the output file
		
		outputFile.write("Leaks:\n\n")
		for x in leak:
			outputFile.write("".join(x) + "\n")
			
		outputFile.write("--------------------\n")
	
	print("[!] Total number of mails:", ct)
	print("[!] Total number of leaked mails:", len(result))	
	print("\n[!] DONE!")
