from version import Version

"""
Contactbook stores many contacts, allowing to perform some operations on them.
"""
class Contactbook:
	def __init__(self, filename=None):
		self.readBook(filename) # We start reading the book in filename.

	"""
	It adds a new contact into self._contacts list.
	@param name: contact's name
	@param phone: contact's phone
	@param email: contact's email
	@param website: contact's website
	@param address: contact's address
	@param city: contact's city
	@param info: contact's info
	@param moment_of_creation: contact's moment of creation. If it's "default", then it's the current of moment of creation.
	@param index: the position of the contact in the self._contacts list. If it's "default", then the contactbook will insert it according to self.descending and self.attrib values. If it's "last", then the contactbook will insert them in the end of the list.
	@return the position of the newly contact in the list
	"""
	def newContact(self, name, phone, email, website, address, city, info, moment_of_creation="default", index="default"):
		if moment_of_creation == "default":
			moment_of_creation = self.cur_momentOfCreation

		contact = {'moment_of_creation': moment_of_creation, 'name': name, 'phone': phone, 'email': email, 'website': website, 'address': address, 'city': city, 'info': info} # First, we create the contact.

		if index == "last":
			self._contacts.append(contact)
			return self.numOfContacts()
		elif index == "default":
			pos = 0

			if self.numOfContacts() != 0:
				if self.descending == False:
					for i in range(self.numOfContacts()):
						if self._contacts[i][self.attrib] < contact[self.attrib]:
							pos += 1
						else:
							break
				else:
					for i in range(self.numOfContacts()):
						if self._contacts[i][self.attrib] > contact[self.attrib]:
							pos += 1
						else:
							break

			self._contacts.insert(pos, contact)
			self.cur_momentOfCreation += 1
			return pos
		else:
			self._contacts.insert(index, contact)
			return self.numOfContacts()

	"""
	It deletes the contact associated to the passed index from the self._contacts list.
	@param index: contact's index in self._contact list.
	"""
	def deleteContact(self, index):
		self._contacts.pop(index)

	"""
	It edits the contact associated to the passed index from the self._contacts list.
	@param index: contact's index.
	@param newName: contact's new name.
	@param newEmail: contact's new email.
	@param newWebsite: contact's new website.
	@param newAddress: contact's new address.
	@param newCity: contact's new city.
	@param newInfo: contact's new additional information.
	"""
	def editContact(self, index, newName, newPhone, newEmail, newWebsite, newAddress, newCity, newInfo):
		self._contacts[index]['name'] = newName
		self._contacts[index]['phone'] = newPhone
		self._contacts[index]['email'] = newEmail
		self._contacts[index]['website'] = newWebsite
		self._contacts[index]['address'] = newAddress
		self._contacts[index]['city'] = newCity
		self._contacts[index]['info'] = newInfo

	"""
	@param index: contact's index
	@return contact's dictionary associated to the passed index.
	"""
	def getContact(self, index):
		return self._contacts[index]

	"""
	It changes the position of the passed contact upward or downard by a step.
	@param index: contact index in self._contacts list.
	@param upward: if True, then the movement is upward. Otherwise, downward.
	"""
	def moveContact(self, index, upward=True):
		if index == 0 and upward == True:
			pass
		elif index == self.numOfContacts()-1 and upward == False:
			pass
		else:
			h = -1 if upward == True else 1

			swap = self._contacts[index+h]
			self._contacts[index+h] = self._contacts[index]
			self._contacts[index] = swap

	"""
	It sorts the contacts in self._contacts list according to a passed attribute.
	@param descending: if True, then the sort order is descending. Otherwise, ascending.
	@param attrib: the attribute
	"""
	def sort(self, descending, attrib):
		self._contacts = sorted(self._contacts, key=lambda d: d[attrib], reverse=descending)

	"""
	It finds contacts in self._contacts list
	@param lookfor: the string to search
	@return a list containing the indices of the found contacts in self._contacts.
	"""
	def find(self, lookfor):
		ret = []

		considering = []

		if self.search_name == True:
			considering.append('name')
		if self.search_phone == True:
			considering.append('phone')
		if self.search_email == True:
			considering.append('email')
		if self.search_website == True:
			considering.append('website')
		if self.search_address == True:
			considering.append('address')
		if self.search_city == True:
			considering.append('city')
		if self.search_info == True:
			considering.append('info')

		for i, j in enumerate(self._contacts):
			k = 0
			while k < len(considering):
				expr = j[considering[k]].lower().find(lookfor.lower()) if self.sensitive == False else j[considering[k]].find(lookfor)

				if expr != -1:
					ret.append(i)
					k = len(considering) # Exit while loop

				k+=1

		return ret

	"""
	@return the number of contacts in self._contacts list.
	"""
	def numOfContacts(self):
		return len(self._contacts)

	"""
	Clear the contactbook.
	"""
	def clear(self):
		self._contacts = []

	"""
	The following two functions, self.newChars and self.oldChars, deal with string manipulation. They are important for .ctcy files, and the reason is above the definition of functions self.saveBook and self.readBook
	"""

	"""
	@param string: the string
	@return the string with commas replaced for \c and new lines replaced for literal \n.
	"""
	def newChars(self, string):
		ret = string.replace('\\c', '\\\c')
		ret = ret.replace(',', '\\c')

		ret = ret.replace('\n', '\\n')

		return ret

	"""
	@param string: the string
	@return the string with \c replaced for commas and literal \n's replaced for new lines.
	"""
	def oldChars(self, string):
		ret = string.replace('\\n', '\n')

		ret = ret.replace('\\c', ',')
		ret = ret.replace('\\\c', '\\c')

		return ret

	"""
	The following two functions, self.saveBook and self.readBook, deal with .ctcy files. These files are organized in this way:

	CONTROL
	[...]
	DATA
	[...]
	
	CONTROL has values for variables. They are version (what version the contactbook was created in), require (starting at what Contacty version can we read the contactbook),
	sensitive (True if using case sensitive for contact searches, False if not), name_search (True if considering name in the contact searches, False if not),
	phone_search (True if considering phone in the contact searches, False if not), email_search (True if considering email in the contact searches, False if not),
	website_search (True if considering website in the contact searches, False if not), address_search (True if considering address in the contact searches, False if not),
	city_search (True if considering city in the contact searches, False if not), info_search (True if considering additional information in the contact searches, False if not),
	descending (True if contacts shall be inserted in descending order, False in ascending), attrib (what attribute to consider for the insertions in ascending or descending order),
	cur_moment_of_creation (the current moment of creation. It will be the value for self.cur_momentOfCreation, an important variable described in self.readBook() function).
	
	DATA has the contact attributes. The attributes are in a .csv style: moment_of_creation,name,phone,email,website,address,city,additional_info.
	Because attributes might have new line and commas, functions self.newChars and self.oldChars are very useful.
	"""

	"""
	It saves the self._contacts list on the passed filename.
	@param filename: the filename
	@return 0 if file could be read. 1 if the version is not compatible.
	"""
	def saveBook(self, filename):
		with open(filename, "w") as f:
			f.write("CONTROL\n")
			v = Version()
			f.write("version=" + v.getVersion() +"\n")
			f.write("require=0.9.0\n")
			f.write("sensitive=" + str(self.sensitive) + "\n")
			f.write("name_search=" + str(self.search_name) + "\n")
			f.write("phone_search=" + str(self.search_phone) + "\n")
			f.write("email_search=" + str(self.search_email) + "\n")
			f.write("website_search=" + str(self.search_website) + "\n")
			f.write("address_search=" + str(self.search_address) + "\n")
			f.write("city_search=" + str(self.search_city) + "\n")
			f.write("info_search=" + str(self.search_info) + "\n")
			f.write("descending=" + str(self.descending) + "\n")
			f.write("attrib=" + str(self.attrib) + "\n")
			f.write("cur_moment_of_creation=" + str(self.cur_momentOfCreation) + "\n")

			f.write("DATA\n")
			for i in self._contacts:
				f.write(str(i['moment_of_creation']) + "," + self.newChars(i['name']) + "," + i['phone'] + "," + i['email'] + "," + i['website'] + "," + self.newChars(i['address']) + "," + self.newChars(i['city']) + "," + self.newChars(i['info']) + '\n')

	"""
	It reads the contact book stored on the passed filename.
	@param filename: the filename. If it is None, then it means a new contact book.
	@return 0 if it was successful, 1 if it requires a newer Contacty version, 2 if the file does not exist and 3 if other error occuried.
	"""
	def readBook(self, filename):
		"""
		Initial procedures:
		"""

		self._contacts = [] # A list of dictionaries. Each dictionary corresponds to a contact, and its keys correspond to the contact attributes (e.g. name)

		"""
		This variable is initially 0 and increase by 1 every time a contact is added. It never decreases. Every contact has a moment of creation, which is equal to the value of self.cur_momentOfCreation in the moment of addition. Its importance is due to the sorting according to the moment of creation.
		"""
		self.cur_momentOfCreation = 0

		"""
		If True, then case sensitive will be used on the searches. If false, then it won't.
		"""
		self.sensitive = False

		"""
		Considering variables for searches:
		"""
		self.search_name = True
		self.search_phone = False
		self.search_email = False
		self.search_website = False
		self.search_address = False
		self.search_city = False
		self.search_info = False

		"""
		Considering variables for adding new contacts:
		"""
		self.descending = False
		self.attrib = 'moment_of_creation'

		"""
		Now the reading itself:
		"""
		if filename != None:
			try:
				startControl = 0
				startData = 0

				nLines = 0 # nLines is the number of lines of filename
				with open(filename, "r") as f:
					for i, j in enumerate(f.readlines()):
						if j == "CONTROL\n":
							startControl = i
						elif j == "DATA\n":
							startData = i
						nLines += 1

				# Handling CONTROL:

				with open(filename, "r") as f:
					for i in f.readlines()[startControl:startData]:
						pos = i.find("=")
						if pos != -1:
							if (i[:pos] == "require"):
									v = Version()
									if v.olderThan(i[pos+1:]):
										return 1
							elif (i[:pos] == "sensitive"):
								self.sensitive = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "name_search"):
								self.search_name = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "phone_search"):
								self.search_phone = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "email_search"):
								self.search_email = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "website_search"):
								self.search_website = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "address_search"):
								self.search_address = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "city_search"):
								self.search_city = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "info_search"):
								self.search_info = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "descending"):
								self.descending = True if i[pos+1:] == "True\n" else False
							elif (i[:pos] == "attrib"):
								self.attrib = i[pos+1:-1]
							elif (i[:pos] == "cur_moment_of_creation"):
								self.cur_momentOfCreation = int(i[pos+1:-1])

				# Handling DATA:

				with open(filename, "r") as f:
					for i in f.readlines()[startData+1:nLines]:
						if i.find(",") != -1:
							j = i.split(",")

							self.newContact(self.oldChars(j[1]), j[2], j[3], j[4], self.oldChars(j[5]), self.oldChars(j[6]), self.oldChars(j[7]), int(j[0]), True)
			except FileNotFoundError as fnf_error:
				return 2
			except:
				return 3

		return 0
