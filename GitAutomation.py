import git
import os
import zipfile
import tarfile

git_url = 'https://github.com/gdabli/PCI_Finder.git'
path = '/Users/gauravdabli/Documents/PCI_Finder'
download_location = '/Users/gauravdabli/Documents/'
tar_name = 'Eboss.tar.gz'

def get_gitRepo():
	if not os.path.exists(path):
		try:
			git.Git(download_location).clone(git_url)
			print ("**** Repository is closed successfully ****")
		except:
			print ("Error downloading repository")
	else:
		print ("Repository is already cloned")

	# perform git pull
	try:
		git_instance = git.cmd.Git(path)
		git_instance.pull()
		print("**** Repository Pulled ****")
	except:
		print("error in pulling git")

	# create zip folder for PCI 
	tar_dir(tar_name, path)		
		
def tar_dir(tar_name,path):
	with tarfile.open(tar_name, "w:gz") as tar_handle:
		for root, dirs, files in os.walk(path):
			for file in files:
				tar_handle.add(os.path.join(root, file))
	print("**** tar created ****")
	    
    	
	    		

if __name__=='__main__':
	get_gitRepo()

			