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
	time.sleep(1)
	print("\n[!] File is being read...")
	time.sleep(1)
	print("[!] Performing requests...\n")
	print("-----------------------\n")
	
	ct = 0
	
	for line in inputFile:
		URL = 'https://haveibeenpwned.com/unifiedsearch/' # request URL
		URL += line # append mail to the URL
		r = requests.get(URL.strip(), headers=headers) # request object
		time.sleep(2) # prevent getting kicked out because of the rate limit
		
		i = 0 # hold index counter
		j = 0 # breach iterator
		breach_ct = 0 # hold breach counter
		
		if r.status_code == 200: # if status code is 200, it means mail is leaked 
			print("[+] Found: ", line)
			result.append(line)
			
			json_object = json.loads(r.text)
			
			for j in json_object['Breaches']:
				breach_ct += 1

			
			for j in range(breach_ct):
				print("Leak", i+1, ":", json_object['Breaches'][i]['Name'], "- Breach Date:", json_object['Breaches'][i]['BreachDate'])
				
				i += 1	
			
			print("\n-----------------------\n")
					
		elif r.status_code == 429:
			print("[!] Seems like you got kicked out because of the rate limit :/")
	
		else:
			print("[-] Not Found: ", line)
			print("-----------------------\n")
		
		ct+=1
	
	print("[!] Total number of mails:", ct)
	print("[!] Total number of leaked mails:", len(result))
	time.sleep(2)
	print("\n[!] DONE!")

	# file output module will be added.
