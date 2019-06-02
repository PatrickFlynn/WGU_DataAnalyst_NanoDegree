import xml.etree.ElementTree as ET
import re
import os

#Home
#filepath = r'S:\Code\School\WGU_DataAnalyst_NanoDegree\02 - Data Wrangling with MongoDB'

#Work
filepath = r'C:\Users\p15144f\Desktop\WGU_DataAnalyst_NanoDegree\02 - Data Wrangling with MongoDB'

osm_file = open(os.path.join(filepath, 'henderson.osm'),
                "r", encoding="utf8")  

#Use regex to get street connector (i.e. ave, st, etc.)
def return_street_connector(street_string):
    street_pattern = re.compile('\s(\w*$)')
    if re.findall(street_pattern, street_string):
        return re.findall(street_pattern, street_string)[0]
    else:
        return ''

#Compare current street connector to expected list
def street_expected_value(str_val):
    street_vals = ['Way', 'Drive', 'Avenue', 'Street', 'Road', 
                   'Lane', 'Parkway', 'Court', 'Highway', 'Trail', 
                   'Boulevard', 'Place', 'Cove']
    return any(str_val == s for s in street_vals)

#Replace targeted errors seen during audit
def replace_func(str_val):
    str_val = re.sub('\s\w{1}$', '', str_val)
    str_val = re.sub('Dr.', 'Drive', str_val)
    str_val = re.sub('Dr$', 'Drive', str_val)
    str_val = re.sub('Rd', 'Road', str_val)
    str_val = re.sub('RD', 'Road', str_val)
    str_val = re.sub('St', 'Street', str_val)
    str_val = re.sub('Ave\.', 'Avenue', str_val)
    return str_val

#Ensure that zip code is 5 digits
def audit_zip_code(postalcode):
    if not re.search('^\d{5}$', postalcode):
        return False
    else:
        return True

#Ensure that coordinates follow Henderson standards
def audit_lat_long(lat, long):
    if not re.search('\d{2}\.\d*', lat):
        return False
    elif not re.search('-\d{3}\.\d*', long):
        return False
    else:
        return True    


def audit(file):
    tree = ET.parse(file)
    root = tree.getroot()
    for elem in root:
        if elem.tag == 'way':
            for tag in elem.iter("tag"):
                #Clean Streets
                if tag.attrib['k'] == 'addr:street' and tag.attrib['v']:
                    if not street_expected_value(return_street_connector(tag.attrib['v'])):
                        print('Dirty Input:', tag.attrib['v'], '---> Sanitized Output:', replace_func(tag.attrib['v']))
                        tag.attrib['v'] = replace_func(tag.attrib['v'])
                
                #Ensure that county is always Clark, NV
                if tag.attrib['k'] == 'tiger:county':
                    if tag.attrib['v'] != 'Clark, NV':
                        print('Error with County! --->', tag.attrib['v'])
                
                #Clean Zip Codes
                if tag.attrib['k'] == 'addr:postcode':
                    if not audit_zip_code(tag.attrib['v']):
                        print(tag.attrib['v'])
                        
        #Check Lat Long to Ensure Integrity
        if elem.tag == 'node':
            if not audit_lat_long(elem.attrib['lat'], elem.attrib['lon']):
                print(elem.attrib['lat'], elem.attrib['lon'])
    #Write new XML file for use in analysis
    tree.write(os.path.join(filepath, 'Cleaned_Henderson.osm'))


if __name__ == '__main__':
    audit(osm_file)
