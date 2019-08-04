##########################################
# Incorrect and inconsistent postal code #
##########################################

#finding the different postal code present in n_tags_pd
n_tags_pd.value[n_tags_pd.key == 'postcode'].unique()
#finding the different postal code present in w_tags_pd
w_tags_pd.value[w_tags_pd.key == 'postcode'].unique()

#function to clean the postcode
def postcode_clean(a):
    b = a.index[a.key == 'postcode'] # finding the index where postcode entires are present
    for i in b: #iterating through the postcode entries
        a.value[i] = a.value[i].replace(' ', '') # removing unnecessary spaces
        if len(a.value[i]) > 6:
            a.value[i] = a.value[i][0]+a.value[i][-5:] # removing extra zeros

#cleaning the n_tags_pd
postcode_clean(n_tags_pd)
n_tags_pd.value[n_tags_pd.key == 'postcode'].unique()
#cleaning the w_tags_pd
postcode_clean(w_tags_pd)
w_tags_pd.value[w_tags_pd.key == 'postcode'].unique()


##########################
# Incorrect House number #
##########################

#different housenumber present 
n_tags_pd[n_tags_pd.key == 'housenumber']
#Details of incorrect house number 
n_tags_pd[n_tags_pd.id == '5450195823']
#Details of incorrect house number 
n_tags_pd[n_tags_pd.id == '4443890291']

#function to clean the house number
def housenumber_clean(a):
    b = a.index[a.key == 'housenumber']
    for i in b:
        a.value[i] = a.value[i].split(',')[0] #removing the street name but keeping the housenumber
        if a.value[i][0] == '+': # finding the phone number
            a.drop(i, axis = 0, inplace = True) #removing the phone number
			
#cleaning the n_tags_pd
housenumber_clean(n_tags_pd)
n_tags_pd[n_tags_pd.key == 'housenumber']


##########################
# Address in street name #
##########################

#different street name present in n_tags_pd
n_tags_pd.value[n_tags_pd.key == 'street'].unique()
#finding details of particular street name
n_tags_pd[n_tags_pd.value == '73 & 75 Rash Behari Avenue']
n_tags_pd[n_tags_pd.id == '1833168504']
#finding details of particular street name
n_tags_pd[n_tags_pd.value == '901A, 9th Floor, Fort Knox, 6, Camac, St. Elgin, Elgin, Kolkata, West Bengal 700017']
n_tags_pd[n_tags_pd.id == '4974928524']


#different street name present in w_tags_pd
w_tags_pd.value[w_tags_pd.key == 'street'].unique()
#finding details of particular street name
w_tags_pd[w_tags_pd.value=='8 Ballygunge Circular Road']
w_tags_pd[w_tags_pd.id == '358854738']
#finding details of particular street name
w_tags_pd[w_tags_pd.value=='4, Gorky Terrace, kolkata- 700017']
w_tags_pd[w_tags_pd.id == '358866967']


#function to clean the street name
def streetname_clean(a):
    b = a.index[a.key == 'street']
    c=[]
    for i in b:
        if (a.value[i].lower().find('kolkata') != -1): #finding 'kolkata'
            if (a.value[i].lower().find('700') !=-1): #finding '700' as postcode for Kolkata start with that
                p = a.value[i].lower().find('700')
                c.append({'id' : a.id[i] , 'key' : 'postcode', 'type': 'addr', 'value': a.value[i][p:p+6]}) # storing all such postcode in 'c'
                
			#removing Kolkata and the part of address following it from street name
            j = a.value[i].lower().find('kolkata') 
            a.value[i] = a.value[i][:j-1]
            a.value[i] = a.value[i].strip(',')
	#adding postcode entries in 'c' to the tag dataframe
    if len(c) != 0:
        a=a.append(c, ignore_index=True)
    return a
	
#cleaning the n_tags_pd
n_tags_pd = streetname_clean(n_tags_pd)
n_tags_pd.value[n_tags_pd.key == 'street'].unique()
n_tags_pd[n_tags_pd.id == '4974928524'] #postcode tag is added

#cleaning the w_tags_pd
w_tags_pd = streetname_clean(w_tags_pd)
w_tags_pd.value[w_tags_pd.key == 'street'].unique()
w_tags_pd[w_tags_pd.id == '358866967'] #postcode tag is added


##########################
# Inconsistent city name #
##########################

#different street name present in n_tags_pd
n_tags_pd.value[n_tags_pd.key == 'city'].unique()
#finding details of particular city name
n_tags_pd[n_tags_pd.value == '700016']

#different street name present in w_tags_pd
w_tags_pd.value[w_tags_pd.key == 'city'].unique()
#finding details of particular city name
w_tags_pd[w_tags_pd.id == '359011649']


#functions to clean city name

def cityname_clean(a):
    b = a.index[a.key == 'city']
    for i in b:
        a.value[i] = a.value[i].split(' ')[0] #removing anything other than city name
        a.value[i] = a.value[i].replace(',','') #removing extra ,
        a.value[i] = a.value[i].capitalize() #making the first letter capital
		
#function to replace city name value with "Kolkata"
def cityname_replace(a):
    b = a.index[a.key == 'city']
    for i in b:
        if a.value[i] != 'Kolkata':
            a.value[i] = 'Kolkata'

# cleaning w_tags_pd
cityname_clean(w_tags_pd)
w_tags_pd.value[w_tags_pd.key == 'city'].unique()

# cleaning n_tags_pd
cityname_clean(n_tags_pd)
cityname_replace(n_tags_pd)
n_tags_pd.value[n_tags_pd.key == 'city'].unique()
