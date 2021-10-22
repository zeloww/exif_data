from io import FileIO
from os import system, makedirs

try:
	from exif import Image

except:
	system("pip install exif")
	from exif import Image

exif = """
███████╗██╗  ██╗██╗███████╗    ██████╗  █████╗ ████████╗ █████╗ 
██╔════╝╚██╗██╔╝██║██╔════╝    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
█████╗   ╚███╔╝ ██║█████╗      ██║  ██║███████║   ██║   ███████║
██╔══╝   ██╔██╗ ██║██╔══╝      ██║  ██║██╔══██║   ██║   ██╔══██║
███████╗██╔╝ ██╗██║██║         ██████╔╝██║  ██║   ██║   ██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝╚═╝         ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
			1 > dir | 4 > delete		by github.com/zeloww
			2 > get | 5 > bytes
		        3 > set | 6 > exit
"""

def _save(image_name:str, image_file:str):
	makedirs(f"exif_modified/", exist_ok=True)
	with open("exif_modified/exif-" + image_name, "wb") as new_image_file:
		new_image_file.write(image_file.get_file())

def _dir(image_name:str):
	with open(image_name, 'rb') as image_file:
		image = Image(image_file)

	result = ""
	dir_list = dir(image)

	for tag in dir_list:
		if not image.get(tag):
			continue

		spaces = ""
		for space in range(32 - len(tag)):
			spaces += " "

		result += "\n{} {} = {}".format(tag, spaces, str(image.get(tag)))

	return result

def _get(image_name:str, tag:str):
	with open(image_name, 'rb') as image_file:
		image = Image(image_file)

	try:
		result = "{} = '{}'".format(tag, image.get(tag))

	except:
		result = "No tag found for '{}'".format(tag)

	return result

def _set(image_name:str, tag:str, value:str):
	with open(image_name, 'rb') as image_file:
		image_file = Image(image_file.read())

	image_file.set(tag, value)
	_save(image_name, image_file)

	result = "Succesfully set '{}' to '{}' in the exif data!".format(tag, value)

	return result 

def _delete(image_name:str, delete_choice):
	with open(image_name, 'rb') as image_file:
		image_file = Image(image_file)

	try:
		if delete_choice.lower() in ["true", "t", "yes", "y", "a", "all"]:
			image_file.delete_all()
			result = "Succesfully delete all exif data!"

		else:
			image_file.delete(delete_choice)

		_save(image_name, image_file)
		result = "Succesfully delete '{}' of the exif data!".format(delete_choice)

	except:
		result = "No exif data named '{}'!".format(delete_choice)

	return result

def _bytes(image_file:str):
	with open(image_file, 'rb') as image_file:
		result = Image(image_file).get_file()

	return result

def main():
	system("color d")

	while True:
		system("cls")
		print(exif)

		try:
			choice = int(input(">>> "))

		except:
			continue

		image_name = input("Enter image file >>> ")

		try:
			FileIO(image_name)

		except FileNotFoundError as e:
			input(e)
			continue

		if choice in [2, 3, 4]:
			with open(image_name, 'rb') as image:
				image = Image(image)

			if not image.has_exif:
				input("Not exif data found!")
				continue

		if choice == 1:
			input(_dir(image_name))

		elif choice == 2:
			tag = input("what tag do you want? (dir for all tag) >>> ")
			input(_get(image_name, tag))

		elif choice == 3:
			tag = input("What tag do you want set? >>> ")
			value = input("New value >>> ")
			input(_set(image_name, tag, value))

		elif choice == 4:
			delete_choice = input("what do you want delete or all? >>> ")
			input(_delete(image_name, delete_choice))

		elif choice == 5:
			input(_bytes(image_name))

		elif choice == 6:
			exit("Bye :D")

if __name__ == "__main__":
	main()