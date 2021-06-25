#!/usr/bin/python3

from __future__ import print_function
import requests, sys, time, json, functools, operator, contextlib

def convertResponse(response): # convert tuple objects into string for sanitized output
	return functools.reduce(operator.add, (response)) 

def main():
	
	print("""
		              _____ _               _    
		             / ____| |             | |   
	 _ ____      ___ __ | |    | |__   ___  ___| | __
	| '_ \ \ /\ / / '_ \| |    | '_ \ / _ \/ __| |/ /
	| |_) \ V  V /| | | | |____| | | |  __/ (__|   < 
	| .__/ \_/\_/ |_| |_|\_____|_| |_|\___|\___|_|\_\ 
	| |                                              
	|_|

	""")

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
		
		lineCount = len(open(sys.argv[1]).readlines( ))
		
		print("\n[!] File is being read...")
		time.sleep(3)
		print("[!] Calculating total number of email addresses...")
		print("[!] Total number of email addresses:", lineCount)
		print("[!] Performing requests...\n")
		print(lineBreaker)
		
		for ct, line in enumerate(inputFile):
			ct += 1
			
			URL = 'https://haveibeenpwned.com/unifiedsearch/' # request URL
			URL += line # append mail to the URL
			r = requests.get(URL.strip(), headers=headers) # request object
			time.sleep(2) # prevent getting kicked out because of the rate limit
			
			i = 0 # hold index counter
			j = 0 # breach iterator
			breach_ct = 0 # hold breach counter
			
			if r.status_code == 200: # if status code is 200, it means mail is leaked 
				succMsg = "[+] {0}/{1} Found: {2}" 
				print(convertResponse(succMsg.format(str(ct), str(lineCount), str(line))))
				result.append(line)
				
				with contextlib.redirect_stdout(outputFile): # redirect result to the output file
					print(lineBreaker)
					print(convertResponse(succMsg.format(str(ct), str(lineCount), str(line))))
	
				json_object = json.loads(r.text)
				
				try:
					iterObj = iter(json_object['Breaches'])
					for j in iterObj: # count breach/breaches
						breach_ct += 1
				except:
					print("Corrupted output! Don't worry, skipping to next email...\n")
					print(lineBreaker) 
					continue
				
				for j in range(breach_ct): # iterate through breach to obtain the data 
					leakMsg = "Leak " + str(i+1) + ": " + json_object['Breaches'][i]['Name'] + " - Breach Date: " + json_object['Breaches'][i]['BreachDate'] # integer to string parsing for concatenation error prevention
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
				notFound = "[-] {0}/{1} Not Found: {2}"
				print(convertResponse(notFound.format(str(ct), str(lineCount), str(line))))
				print(lineBreaker)
				
			ct += 1
		
		firstResult = "[!] Total number of email addresses: ", str(lineCount)
		print(convertResponse(firstResult))
		
		secondResult = "[!] Total number of leaked email addresses: ", str(len(result))
		print(convertResponse(secondResult))
		
		with contextlib.redirect_stdout(outputFile): # redirect result to the output file
			print(lineBreaker)
			print(convertResponse(firstResult))
			print(convertResponse(secondResult))
		
		print("\nPwned mails & breach information are written into:", sys.argv[2])
		print("\n[!] DONE!")

if len(sys.argv) < 2:
	print("\nType -h or --help for usage menu.\n")
elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
	print("\nUsage:")
	print("	\n# python3 pwnCheck.py <MAIL_LIST> <OUTPUT_FILE_NAME>\n")
elif len(sys.argv) > 3 and sys.argv[1] != "-h" and sys.argv[1] != "--help":
	print("\nToo many parameters amigo, try again.\n")
else:
	main()
