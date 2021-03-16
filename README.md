# pwnCheck

## Description

This tool is using **[Have I Been Pwned](https://haveibeenpwned.com)** service for queries and it will help you to automate your scans during your pentest(s).

----------------------

## Usage

Usage of this tool is pretty simple. 

Just give the path for your mail list and a name (to create the output file on the path that you are currently on) or full path for your output file & you are good to go!

### Option #1:

```
# pwnCheck <mail_list> <output_file_name>
```

### Option #2:

``` 
# pwnCheck </path/mail_list> </path/output_file_name>
``` 

### Important Note:

If you want to run this program from any path on the system, just add a link for it:

```
ln -s /path/pwnCheck /usr/local/bin
``` 
----------------------

## Sample Run

### Running the tool:

<p align="center"><img src="https://i.hizliresim.com/8ZlDoT.png"></p>

### Output file:

<p align="center"><img src="https://i.hizliresim.com/uCr2t6.png"></p>
