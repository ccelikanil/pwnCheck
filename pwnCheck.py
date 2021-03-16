#!/usr/bin/python3

import requests, sys, time, json, functools, operator, contextlib

def convertResponse(response): # convert tuple objects into string for sanitized output
	return functools.reduce(operator.add, (response)) 

def main():
	headers = {
		'User-Agent': 'agent_smith',
		'Accept': 'accept_em_all',
		'Accept-Language': 'language',
		'Cookie': 'cookie_monster'
	}

	result = []
	lineBreaker = "-----------------------\n"

	with open(sys.argv[1], 'r') as inputFile:
		outputFile = open(sys.argv[2], 'w')
		time.sleep(1)
		print("\n[!] File is being read...")
		time.sleep(1)
		print("[!] Performing requests...\n")
		print(lineBreaker)
		
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
				succMsg = "[+] Found: ", line
				print(convertResponse(succMsg))
				result.append(line)
				
				with contextlib.redirect_stdout(outputFile): # redirect result to the output file
					print(lineBreaker)
					print(convertResponse(succMsg))
	
				json_object = json.loads(r.text)
				
				for j in json_object['Breaches']: # count breach/breaches
					breach_ct += 1
				
				for j in range(breach_ct): # iterate through breach to obtain the data 
					leakMsg = "Leak ", str(i+1), ": ", json_object['Breaches'][i]['Name'], " - Breach Date: ", json_object['Breaches'][i]['BreachDate'] # integer to string parsing for concatenation error prevention
					print(convertResponse(leakMsg))
					
					with contextlib.redirect_stdout(outputFile): # redirect result to the output file
						print(convertResponse(leakMsg))
				
					i += 1	
				
				print()
				with contextlib.redirect_stdout(outputFile):
					print()		
				
				print(lineBreaker)
							
			elif r.status_code == 429:
				limitMsg = "[!] This isn't supposed to be happening but seems like you got kicked out because of the rate limit :/ (Status Code: 429)" 
				print(limitMsg)
		
			else:
				notFound = "[-] Not Found: ", line
				print(convertResponse(notFound))
				print(lineBreaker)
			
			ct+=1
		
		firstResult = "[!] Total number of mails: ", str(ct)
		print(convertResponse(firstResult))
		
		secondResult = "[!] Total number of leaked mails: ", str(len(result))
		print(convertResponse(secondResult))
		
		with contextlib.redirect_stdout(outputFile): # redirect result to the output file
			print(lineBreaker)
			print(convertResponse(firstResult))
			print(convertResponse(secondResult))
		
		print("\nPwned mails & breach information are written into:", sys.argv[2])
		
		time.sleep(2)
	
		print("\n[!] DONE!")
main()
