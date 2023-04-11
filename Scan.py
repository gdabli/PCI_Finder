import boto3
import smart_open
import re

'''
This is simple python utility that scans objects inside a given S3 bucket for any PCI data on it. 
'''

''' Constants for SSN and Email '''
SSN = r'^(\d{3}-\d{2}-\d{4}|XXX-XX-XXXX)$'
EMAIL = r'^[\w.-]+@[\w.-]+$'

''' Constants for Personal Account Numbers '''
VISA = r'4[0-9]{12}(?:[0-9]{3})?$'
MASTERCRD = r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$'
AMEX = r'^3[47][0-9]{13}$'
DISCOVER = r'^6(?:011|5[0-9]{2})[0-9]{12}$'
DINERCLUB = r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$'
PAN = r'^\D(\d{5})\D$'

def main():
	ext = [".csv", ".txt", ".xls", ".xlsx", ".dat"]
	objects_list = get_s3_objects('bucket-name')
	for file_path in objects_list:
		if file_path.endwith(tuple(ext)):
			search_pci(file_path)


'''Get list of S3 objects in given bucket '''
def get_s3_objects(bucket):
	keys = []
	kwargs = {'Bucket': bucket}
	s3 = boto3.client('s3')

	while True:
		resp = s3.list_objects_v2(**kwargs)
		for obj in resp['Contents']:
			keys.append(obj['Key'])

		try:
			kwargs['ContinuationToken']	= resp['NextContinuationToken']
		except KeyError:
			break

''' search all pci data in given file '''
def search_pci(file_path):
	file_path = "S3://bucket-name/" + file_path
	print file_path
	Output=open("output.txt", "a+")

	for line in smart_open.smart_open(file_path):
		check = "NO"
		content_list = line.split(" ")
		for content in content_list:
			if re.search("|".join([SSN, VISA, MASTERCRD, AMEX, DISCOVER, DINERCLUB, EMAIL, PAN]), content):
				print "FOUND: " + file_path
				check = "YES"
				Output.write(file_path + "\n")
				Output.close()
			if check == "YES":
				break

if __name__ == '__main__':
	main()
