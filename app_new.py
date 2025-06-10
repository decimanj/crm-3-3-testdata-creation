import streamlit as st
import random
import string
import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re
import uuid

st.set_page_config(page_title="CRM 3.3 Staging Test Data Creation Tools")

# Load external CSS
with open("style.css", "r") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Check if this is the first load
if "first_load" not in st.session_state:
    st.session_state.first_load = True
    with st.spinner("## Developed by Deciman Julius"):
        import time
        time.sleep(2)  # Simulate loading delay
else:
    st.session_state.first_load = False  # Ensure the spinner doesn't show again

# Utility functions
def format_date_yymmdd(date):
    year = str(date.year)[-2:]
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    return f"{year}{month}{day}"

def random_string(length, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def random_char():
    chars = string.ascii_letters
    return random.choice(chars)

def random_name():
    names = [
        'John', 'Jane', 'Alex', 'Emma', 'Michael', 'Sarah', 'David', 'Lisa', 'Chris', 'Anna', 'James', 'Emily', 'Robert', 'Sophie', 'William', 'Olivia', 'Thomas', 'Grace', 'Daniel', 'Chloe', 'Matthew', 'Isabella', 'Andrew', 'Mia', 'Steven', 'Lily', 'Mark', 'Hannah', 'Paul', 'Julia', 'Richard', 'Amelia', 'Charles', 'Ella', 'George', 'Ava', 'Joseph', 'Charlotte', 'Edward', 'Lucy', 'Benjamin', 'Zoe', 'Samuel', 'Abigail', 'Henry', 'Sophia', 'Jack', 'Madison', 'Luke', 'Natalie', 'Ryan', 'Evelyn', 'Ethan', 'Victoria', 'Nathan', 'Isabelle', 'Adam', 'Lillian', 'Joshua', 'Scarlett', 'Peter', 'Aria', 'Jacob', 'Samantha', 'Isaac', 'Ruby', 'Liam', 'Gabriella', 'Noah', 'Harper', 'Logan', 'Avery', 'Elijah', 'Mila', 'Mason', 'Sofia', 'Caleb', 'Eleanor', 'Owen', 'Audrey', 'Dylan', 'Claire', 'Lucas', 'Violet', 'Gabriel', 'Hazel', 'Julian', 'Penelope', 'Levi', 'Stella', 'Carter', 'Layla', 'Wyatt', 'Aurora', 'Connor', 'Savannah', 'Evan', 'Brooklyn', 'Dominic', 'Addison', 'Hunter', 'Paisley', 'Nicholas', 'Aiden', 'Zachary', 'Aubrey', 'Tyler', 'Skylar', 'Brandon', 'Mackenzie', 'Jonathan', 'Leah', 'Christian', 'Lydia', 'Austin', 'Kayla', 'Colin', 'Morgan', 'Cameron', 'Hailey', 'Patrick', 'Sadie', 'Ian', 'Allison', 'Eric', 'Madelyn', 'Timothy', 'Naomi', 'Kevin', 'Autumn', 'Sean', 'Jocelyn', 'Brian', 'Jasmine', 'Justin', 'Valentina', 'Jordan', 'Katherine', 'Kyle', 'Esme', 'Aaron', 'Delilah', 'Brayden', 'Norah', 'Vincent', 'Faith', 'Tristan', 'Lauren', 'Xavier', 'Ivy', 'Devin', 'Lila', 'Elliot', 'Rose', 'Finn', 'Peyton', 'Gavin', 'Jade', 'Hayden', 'Hadley', 'Joel', 'Ember', 'Miles', 'Elise', 'Parker', 'Piper', 'Roman', 'Aria', 'Shane', 'Celeste', 'Tucker', 'Freya', 'Victor', 'June', 'Wesley', 'Marissa', 'Adrian', 'Brianna', 'Ashton', 'Tessa', 'Blake', 'Kaitlyn', 'Clayton', 'Giselle', 'Cody', 'Maeve', 'Damian', 'Iris', 'Declan', 'Juliana', 'Derek', 'Serena', 'Ezra', 'Angelina', 'Felix', 'Clara', 'Garrett', 'Adeline', 'Grayson', 'Beatrice', 'Harrison', 'Daisy', 'Hudson', 'Evangeline', 'Jace', 'Opal', 'Jasper', 'Lola', 'Jensen', 'Willow', 'Knox', 'Mabel', 'Landon', 'Esther', 'Leo', 'Cora', 'Lincoln', 'Lyric', 'Micah', 'Eloise', 'Nolan', 'Amara', 'Preston', 'Rosalie', 'Reid', 'Genevieve', 'Rhett', 'Anastasia', 'Sawyer', 'Blair', 'Silas', 'Sienna', 'Tanner', 'Marley', 'Theo', 'Nadia', 'Tobias', 'Lena', 'Trevor', 'Elsie', 'Vaughn', 'Ramona', 'Walker', 'Olive', 'Weston', 'Gemma', 'Zane', 'Astrid', 'Abel', 'Bryn', 'Alden', 'Carmen', 'Amos', 'Eliza', 'Archer', 'Fern', 'Barrett', 'Greta', 'Beckett', 'Hallie', 'Bennett', 'Ingrid', 'Brock', 'Josie', 'Cade', 'Kiera', 'Callan', 'Lacey', 'Cedric', 'Mira', 'Clark', 'Noelle', 'Colton', 'Poppy', 'Conor', 'Reese', 'Cooper', 'Selena', 'Dane', 'Talia', 'Dante', 'Uma', 'Darius', 'Vera', 'Dillon', 'Wren', 'Drake', 'Yara', 'Elias', 'Zara', 'Emmett', 'Alana', 'Everett', 'Bianca', 'Fabian', 'Cecilia', 'Flynn', 'Daphne', 'Forrest', 'Emery', 'Gideon', 'Fiona', 'Graham', 'Gloria', 'Grant', 'Helen', 'Hank', 'Imogen', 'Holden', 'Juniper', 'Hugo', 'Kinsley', 'Ivan', 'Lara', 'Jett', 'Mina', 'Jonah', 'Nora', 'Judah', 'Ophelia', 'Kane', 'Quinn', 'Keegan', 'Rhea', 'Kieran', 'Sabrina', 'Lance', 'Thea', 'Lennon', 'Vienna', 'Leon', 'Winnie', 'Malcolm', 'Xena', 'Milo', 'Yasmin', 'Neil', 'Zelda', 'Nico', 'Aisha', 'Orion', 'Bria', 'Oscar', 'Celine', 'Otto', 'Dina', 'Percy', 'Elsa', 'Quentin', 'Farah', 'Remy', 'Gia', 'Rory', 'Hana', 'Russell', 'Ida', 'Ryder', 'Jada', 'Soren', 'Kara', 'Spencer', 'Lana', 'Tate', 'Mara', 'Thane', 'Nia', 'Titus', 'Oona', 'Travis', 'Phoebe', 'Troy', 'Roxanne', 'Vance', 'Sasha', 'Walter', 'Tina', 'Warren', 'Uma', 'Wilson', 'Vera', 'Winston', 'Wendy', 'Xander', 'Xena', 'Yusuf', 'Yara', 'Zachariah', 'Zoe', 'Aaron', 'Amaya', 'Alvin', 'Anya', 'Andre', 'Aspen', 'Angelo', 'Belen', 'Arthur', 'Cali', 'Asher', 'Dana', 'Atticus', 'Eden', 'Axl', 'Faye', 'Baxter', 'Gina', 'Beau', 'Haven', 'Benson', 'Indie', 'Bodie', 'Jolie', 'Brady', 'Kaya', 'Brecken', 'Livia', 'Brody', 'Maia', 'Bryce', 'Nadine', 'Cairo', 'Oria', 'Calvin', 'Paloma', 'Camden', 'Qiana', 'Cannon', 'Riva', 'Carson', 'Sana', 'Casper', 'Tara', 'Chandler', 'Ursula', 'Chase', 'Vada', 'Chester', 'Willa', 'Cillian', 'Xyla', 'Clifford', 'Yana', 'Clyde', 'Zaria', 'Cohen', 'Alma', 'Corey', 'Brynlee', 'Cruz', 'Cleo', 'Cyrus', 'Demi', 'Dallas', 'Eira', 'Damon', 'Fiona', 'Dax', 'Gwendolyn', 'Dean', 'Hattie', 'Denver', 'Ila', 'Dexter', 'Jessa', 'Donovan', 'Kendra', 'Drew', 'Lila', 'Duke', 'Mavis', 'Easton', 'Nell', 'Eden', 'Odelia', 'Edison', 'Petra', 'Egan', 'Quincy', 'Eli', 'Raven', 'Ellis', 'Sloan', 'Elvis', 'Tatum', 'Emerson', 'Uma', 'Enzo', 'Vesper', 'Ezra', 'Wendy', 'Finnick', 'Xena', 'Fletcher', 'Yvette', 'Ford', 'Zinnia', 'Franklin', 'Avery', 'Gage', 'Blaire', 'Gareth', 'Callie', 'Gatlin', 'Delphine', 'Grady', 'Elowen', 'Gunnar', 'Frida', 'Hassan', 'Giada', 'Heath', 'Hazel', 'Hector', 'Iona', 'Homer', 'Jana', 'Idris', 'Kallie', 'Ignacio', 'Lark', 'Ira', 'Mae', 'Ismael', 'Nessa', 'Jagger', 'Oona', 'Jairo', 'Pilar', 'Jared', 'Rory', 'Jensen', 'Siena', 'Jett', 'Tia', 'Joaquin', 'Vida', 'Jonas', 'Wynter', 'Jude', 'Xena', 'Kaden', 'Yara', 'Khalil', 'Zoe'
    ]
    return random.choice(names)

def random_id_number(dob=None):
    dob = dob or random_date_of_birth()
    yymmdd = dob[2:]  # Extract YYMMDD from YYYYMMDD
    xx = str(random.randint(1, 12)).zfill(2)
    xxxx = str(random.randint(0, 9999)).zfill(4)
    return f"{yymmdd}{xx}{xxxx}"

def random_date_of_birth():
    end = datetime.date(2007, 4, 25)  # 18 years before today (2025-04-25)
    start = datetime.date(1990, 1, 1)  # 35 Years Max
    diff = (end - start).days
    random_days = random.randint(0, diff)
    random_date = start + datetime.timedelta(days=random_days)
    return f"{random_date.year}{random_date.month:02d}{random_date.day:02d}"

def random_transaction_id():
    letters = string.ascii_uppercase
    digits = string.digits
    return (
        random_string(3, letters) +
        random_string(5, digits) +
        random_string(1, letters)
    )

def random_customer_id():
    random8 = str(random.randint(0, 99999999)).zfill(8)
    return f"10000{random8}"

def parse_msisdn_output(xml_output):
    try:
        root = ET.fromstring(xml_output)
        msisdns = []
        for msisdn_elem in root.findall(".//sch:msisdn", namespaces={"sch": "http://oss.huawei.com/webservice/external/services/schema"}):
            msisdn = msisdn_elem.text
            if msisdn and msisdn.isdigit() and 10 <= len(msisdn) <= 12:
                msisdns.append(msisdn)
        return msisdns
    except Exception as e:
        st.error(f"Failed to parse MSISDN XML: {str(e)}")
        return []

def parse_iccid_imsi_output(sql_output):
    try:
        lines = sql_output.strip().split("\n")
        data = []
        for line in lines:
            if line.strip():
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 3:
                    iccid, imsi, _ = parts[:3]
                    if iccid.isdigit() and 19 <= len(iccid) <= 20 and imsi.isdigit() and len(imsi) == 15:
                        data.append({"iccid": iccid, "imsi": imsi})
        return data
    except Exception as e:
        st.error(f"Failed to parse ICCID/IMSI output: {str(e)}")
        return []

def generate_dummy_data(index):
    dob = random_date_of_birth()
    return {
        "accessSessionRequest": {
            "accessChannel": "10050",
            "operatorCode": "CSG",
            "password": "PkzVHH0odLylDCRIPJM+Mw==",
            "beId": "102",
            "version": "1",
            "transactionId": random_transaction_id(),
            "remoteAddress": ""
        },
        "customerInfo": {
            "customerId": random_customer_id(),
            "customerFlag": "1",
            "subscriberType": "",
            "customerCode": random_string(8),
            "idType": "1",
            "idNumber": random_id_number(dob),
            "expiryDateofcertificate": "20300101",
            "title": "21",
            "firstName": random_name() + random_char() * 2,
            "middleName": "SemiAutoTest",
            "lastName": random_char() * 4,
            "nationality": "1458",
            "customerLang": "2",
            "customerLevel": "9",
            "customerGroup": "0",
            "race": "1",
            "occupation": "2",
            "customerDateofBirth": dob,
            "customerGender": "1",
            "maritalStatus": "0",
            "customerStatus": "A02",
            "customerAddressInfos": [{
                "contactType": "3",
                "address1": "Testing Address",
                "address2": "CelcomDigi Hub",
                "address3": "address3",
                "addressCountry": "1458",
                "addressProvince": "MYS_14",
                "overseasProvince": "MYS_14",
                "addressCity": "c421",
                "addressPostCode": "02600",
                "email1": f"dummy{index}@digi.com.my",
                "smsNo": "60104661007",
                "info1": "cust1",
                "info2": "cust2",
                "info3": "cust3",
                "info4": "cust4",
                "info5": "cust5"
            }],
            "customerRelationInfos": [{
                "relaSeq": "1",
                "relaType": "2",
                "relaPriority": "1",
                "relaName1": "REL1",
                "relaName2": "REL2",
                "relaName3": "REL3",
                "relaTel1": "1",
                "relaTel2": "1",
                "relaTel3": "1",
                "relaTel4": "1",
                "relaEmail": f"rel{index}@digi.com",
                "relaFax": "1",
                "beginTimeForBusiDay": "1111",
                "endTimeForBusiDay": "1111",
                "beginTimeForWeekend": "1111",
                "endTimeForWeekend": "1111",
                "info1": "1",
                "info2": "1",
                "info3": "1"
            }],
            "corporationInfo": {
                "corpNumber": "1",
                "companyName": "COMPANY1",
                "shortName": "COMP1",
                "hierarchy": "1",
                "topParentCustomerId": "1",
                "parentCustomerId": "1",
                "businessRegistrationNumber": "1",
                "expiryDateofBRN": "11111111",
                "ownershipType": "1",
                "industrySegment": "1",
                "businessNature": "201",
                "phoneNumber": "60104661007",
                "email": f"corp{index}@digi.com",
                "fax": "1",
                "geographicalSpread": "1",
                "telcoProviders": "1",
                "sow": "4",
                "accountValue": "1",
                "dateofIncorporation": "11111111",
                "numberofEmployees": "1",
                "paidupCapital": "1",
                "salesTurnover": "1",
                "enterpriseCustomerType": "1",
                "remark": "CORP_REMARK",
                "subCustomerList": [{"customerId": "1", "companyName": "SUB1"}],
                "picInfos": [{
                    "picSeq": "1",
                    "name": "PIC1",
                    "title": "1",
                    "gender": "1",
                    "race": "1",
                    "phoneNumber": "1",
                    "email": f"pic{index}@digi.com",
                    "dateofBirth": "11111111",
                    "isNotificationPerson": "1",
                    "picType": "1",
                    "idType": "15",
                    "idNumber": "1",
                    "nationality": "1458"
                }],
                "accountManagerInfo": {
                    "name": "MANAGER1",
                    "phoneNumber": "1",
                    "email": f"manager{index}@digi.com",
                    "salesmanCode": "1",
                    "dealerCode": "R0001-B0001"
                }
            },
            "numOfSubPerCondition": "1",
            "info1": "info1",
            "info2": "info2",
            "info3": "info3",
            "info4": "info4",
            "info5": "info5"
        },
        "newAcctSubscriberInfos": [{
            "accountInfo": {
                "accountId": "4000011111",
                "customerId": random_customer_id(),
                "accountCode": "1",
                "billcycleType": "04",
                "title": "3",
                "accountName": f"TEST_ACCOUNT_{index}",
                "converge_flag": "",
                "billLanguage": "2",
                "initialCreditLimit": "10000",
                "status": "0",
                "creditLimitNotifyPercentages": ["4", "7"],
                "acla": "0",
                "noDunningFlag": "0",
                "loyaltyCardNo": "1234567",
                "creditTerm": "1",
                "isAutoReload": "false",
                "email": f"account{index}@digi.com.my",
                "isPaymentResponsible": "true",
                "addressInfo": [{
                    "contactType": "4",
                    "address1": "Testing Address",
                    "address2": "CelcomDigi Hub",
                    "address3": "address3",
                    "addressCountry": "1458",
                    "addressProvince": "MYS_14",
                    "overseasProvince": "MYS_14",
                    "addressCity": "c421",
                    "addressPostCode": "02600",
                    "email1": f"account{index}@digi.com.my",
                    "smsNo": "60104661007",
                    "info1": "addressinfo1",
                    "info2": "addressinfo2",
                    "info3": "addressinfo3",
                    "info4": "addressinfo4",
                    "info5": "addressinfo5"
                }],
                "paymentModeInfo": {
                    "paymentId": "1",
                    "paymentMode": "CASH",
                    "cardType": "1",
                    "ownerName": "OWNER1",
                    "bankCode": "CITIBANK",
                    "bankAcctNo": random_string(32) + "=",
                    "ownershipType": "1",
                    "bankIssuer": "CITIBANK",
                    "cardExpDate": "20330101"
                },
                "info1": "acctinfo1",
                "info2": "60104661007",
                "info3": "acctinfo3",
                "info4": "acctinfo4",
                "info5": "acctinfo5"
            },
            "billMediumInfos": [{
                "billMediumId": "1003",
                "orderedSeqId": "1"
            }],
            "newSubscriberInfos": {
                "subscriberCountSeq": str(index),
                "subscriberInfo": {
                    "subscriberId": "1",
                    "customerId": random_customer_id(),
                    "paidFlag": "",
                    "subscriberType": "1",
                    "msisdn": "",
                    "imsi": "",
                    "iccid": "",
                    "imei": "2",
                    "subscriberLanguage": "2",
                    "suspensionResumeReason": "1",
                    "subscriberSegment": "4",
                    "companyName": "compan1",
                    "companyIndustry": "20",
                    "businessNature": "202",
                    "corporateName": "corpor5",
                    "userName": "userName",
                    "subscriberStatus": "B01",
                    "createDate": "11111111111111",
                    "effectiveDate": "11111111111111",
                    "expiryDate": "11111111111111",
                    "latestActivationDate": "11111111111111",
                    "activeDate": "11111111111111",
                    "defaultAcctId": f"40000{random_string(7)}",
                    "telecomType": "",
                    "finalCLQuota": "123",
                    "tempCLQuota": "456",
                    "isUseOverPayment": "1",
                    "creditLimitNotifyPercentages": ["5"],
                    "smsNotifySettingInfos": [{
                        "eventType": "6",
                        "openFlag": "true"
                    }],
                    "tenure": "30",
                    "otherRelaAccts": [{
                        "subscriberId": "1",
                        "relaType": "2"
                    }]
                },
                "primaryOfferInfo": {
                    "offerId": ""
                }
            }
        }],
        "transactionCommonInfo": {
            "isPendingQApproved": "true",
            "remark": ""
        }
    }

def generate_soap_xml(data_sets):
    envelope = ET.Element("soapenv:Envelope", {
        "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "xmlns:sch": "http://oss.huawei.com/webservice/external/services/schema",
        "xmlns:bas": "http://oss.huawei.com/webservice/external/services/basetype/"
    })
    header = ET.SubElement(envelope, "soapenv:Header")
    body = ET.SubElement(envelope, "soapenv:Body")
    create_new_subscriber = ET.SubElement(body, "sch:createNewSubscriber")
    
    # AccessSessionRequest
    access_session = ET.SubElement(create_new_subscriber, "sch:AccessSessionRequest")
    for key, value in data_sets[0]["accessSessionRequest"].items():
        if key != "remoteAddress":
            ET.SubElement(access_session, f"bas:{key}").text = value
    access_session.append(ET.Comment(f"<bas:remoteAddress>{data_sets[0]['accessSessionRequest']['remoteAddress']}</bas:remoteAddress>"))
    
    # CreateNewSubscriberRequest
    create_request = ET.SubElement(create_new_subscriber, "sch:CreateNewSubscriberRequest")
    customer_info = ET.SubElement(create_request, "sch:customerInfo")
    
    # Customer Info with specific fields commented
    customer_info_fields = data_sets[0]["customerInfo"]
    # Define the order of fields to ensure consistency
    customer_info_fields_order = [
        "customerId", "customerFlag", "subscriberType", "customerCode", "idType", 
        "idNumber", "expiryDateofcertificate", "title", "firstName", "middleName", 
        "lastName", "nationality", "customerLang", "customerLevel", "customerGroup", 
        "race", "occupation", "customerDateofBirth", "customerGender", "maritalStatus", 
        "customerStatus"
    ]
    for key in customer_info_fields_order:
        if key in customer_info_fields:
            if isinstance(customer_info_fields[key], str):
                if key == "customerId":
                    customer_info.append(ET.Comment(f"Randomized 13-digit customerId starting with 10000 \n                    <bas:customerId>{customer_info_fields[key]}</bas:customerId>"))
                elif key == "customerCode":
                    customer_info.append(ET.Comment(f"Customer code <bas:customerCode>{customer_info_fields[key]}</bas:customerCode>"))
                elif key == "subscriberType":
                    customer_info.append(ET.Comment(f"<bas:subscriberType>{customer_info_fields[key]}</bas:subscriberType>"))
                else:
                    ET.SubElement(customer_info, f"bas:{key}").text = customer_info_fields[key]
    
    # Add customerSegment with a preceding comment
    customer_info_children = list(customer_info)
    insert_index = None
    for idx, child in enumerate(customer_info_children):
        if child.tag == "bas:customerGroup":
            insert_index = idx
            break
    if insert_index is None:
        insert_index = len(customer_info_children)
    customer_info.insert(insert_index, ET.Comment("Customer segment"))
    customer_segment = ET.Element("bas:customerSegment")
    customer_segment.text = "SEG1"
    customer_info.insert(insert_index + 1, customer_segment)
    
    # Add createDate comment after maritalStatus
    for idx, child in enumerate(list(customer_info)):
        if child.tag == "bas:maritalStatus":
            customer_info.insert(idx + 1, ET.Comment(f"Create date  <bas:createDate>{format_date_yymmdd(datetime.date.today())}</bas:createDate>"))
            break
    
    # Customer Address Infos
    for addr in data_sets[0]["customerInfo"]["customerAddressInfos"]:
        addr_info = ET.SubElement(customer_info, "bas:customerAddressInfos")
        for key, value in addr.items():
            ET.SubElement(addr_info, f"bas:{key}").text = value
    
    # Customer Relation Infos
    for rel in data_sets[0]["customerInfo"]["customerRelationInfos"]:
        rel_info = ET.SubElement(customer_info, "bas:customerRelationInfos")
        for key, value in rel.items():
            ET.SubElement(rel_info, f"bas:{key}").text = value
    
    # Corporation Info with correct order
    corp_info = ET.SubElement(customer_info, "bas:corporationInfo")
    corp_fields_order = [
        "corpNumber", "companyName", "shortName", "hierarchy", "topParentCustomerId",
        "parentCustomerId", "subCustomerList", "businessRegistrationNumber", "expiryDateofBRN",
        "ownershipType", "industrySegment", "businessNature", "phoneNumber", "email",
        "fax", "geographicalSpread", "telcoProviders", "sow", "accountValue",
        "dateofIncorporation", "numberofEmployees", "paidupCapital", "salesTurnover",
        "enterpriseCustomerType", "remark", "picInfos", "accountManagerInfo"
    ]
    for key in corp_fields_order:
        if key in data_sets[0]["customerInfo"]["corporationInfo"]:
            if key == "subCustomerList":
                for sub in data_sets[0]["customerInfo"]["corporationInfo"]["subCustomerList"]:
                    sub_list = ET.SubElement(corp_info, "bas:subCustomerList")
                    for sub_key, sub_value in sub.items():
                        ET.SubElement(sub_list, f"bas:{sub_key}").text = sub_value
            elif key == "picInfos":
                for pic in data_sets[0]["customerInfo"]["corporationInfo"]["picInfos"]:
                    pic_info = ET.SubElement(corp_info, "bas:picInfos")
                    for pic_key, pic_value in pic.items():
                        ET.SubElement(pic_info, f"bas:{pic_key}").text = pic_value
            elif key == "accountManagerInfo":
                account_manager = ET.SubElement(corp_info, "bas:accountManagerInfo")
                for am_key, am_value in data_sets[0]["customerInfo"]["corporationInfo"]["accountManagerInfo"].items():
                    ET.SubElement(account_manager, f"bas:{am_key}").text = am_value
            else:
                ET.SubElement(corp_info, f"bas:{key}").text = data_sets[0]["customerInfo"]["corporationInfo"][key]
    
    # Add numOfSubPerCondition and info1 to info5 at the end
    for key in ["numOfSubPerCondition", "info1", "info2", "info3", "info4", "info5"]:
        ET.SubElement(customer_info, f"bas:{key}").text = data_sets[0]["customerInfo"][key]
    
    # New Acct Subscriber Infos
    for data in data_sets:
        new_acct = ET.SubElement(create_request, "sch:newAcctSubscriberInfos")
        account_info = ET.SubElement(new_acct, "bas:accountInfo")
        account_info_fields = data["newAcctSubscriberInfos"][0]["accountInfo"]
        account_fields_order = [
            "accountId", "customerId", "accountCode", "billcycleType", "title",
            "accountName", "converge_flag", "billLanguage", "initialCreditLimit", "status",
            "creditLimitNotifyPercentages", "acla", "noDunningFlag", "loyaltyCardNo",
            "creditTerm", "isAutoReload", "email", "isPaymentResponsible",
            "addressInfo", "paymentModeInfo", "info1", "info2", "info3", "info4", "info5"
        ]
        for key in account_fields_order:
            if key in account_info_fields:
                if key == "accountId":
                    account_info.append(ET.Comment(f"<bas:accountId>{account_info_fields['accountId']}</bas:accountId>"))
                elif key == "customerId":
                    account_info.append(ET.Comment(f"<bas:customerId>{account_info_fields['customerId']}</bas:customerId>"))
                elif key == "creditLimitNotifyPercentages":
                    for p in account_info_fields["creditLimitNotifyPercentages"]:
                        ET.SubElement(account_info, "bas:creditLimitNotifyPercentages").text = p
                elif key == "addressInfo":
                    for addr in account_info_fields["addressInfo"]:
                        addr_info = ET.SubElement(account_info, "bas:addressInfo")
                        for addr_key, addr_value in addr.items():
                            ET.SubElement(addr_info, f"bas:{addr_key}").text = addr_value
                elif key == "paymentModeInfo":
                    payment_mode = ET.SubElement(account_info, "bas:paymentModeInfo")
                    for pm_key, pm_value in account_info_fields["paymentModeInfo"].items():
                        if pm_key in ["bankCode", "bankAcctNo", "bankIssuer"]:
                            payment_mode.append(ET.Comment(f"<bas:{pm_key}>{pm_value}</bas:{pm_key}>"))
                        else:
                            ET.SubElement(payment_mode, f"bas:{pm_key}").text = pm_value
                else:
                    ET.SubElement(account_info, f"bas:{key}").text = account_info_fields[key]
        
        for bill in data["newAcctSubscriberInfos"][0]["billMediumInfos"]:
            bill_info = ET.SubElement(new_acct, "bas:billMediumInfos")
            for key, value in bill.items():
                ET.SubElement(bill_info, f"bas:{key}").text = value
        
        new_subscriber = ET.SubElement(new_acct, "bas:newSubscriberInfos")
        ET.SubElement(new_subscriber, "bas:subscriberCountSeq").text = data["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberCountSeq"]
        subscriber_info = ET.SubElement(new_subscriber, "bas:subscriberInfo")
        subscriber_info_fields = data["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberInfo"]
        subscriber_fields_order = [
            "subscriberId", "customerId", "paidFlag", "subscriberType", "msisdn",
            "imsi", "iccid", "imei", "subscriberLanguage", "suspensionResumeReason",
            "subscriberSegment", "companyName", "companyIndustry", "businessNature",
            "corporateName", "userName", "subscriberStatus", "createDate", "effectiveDate",
            "expiryDate", "latestActivationDate", "activeDate", "defaultAcctId",
            "telecomType", "finalCLQuota", "tempCLQuota", "isUseOverPayment",
            "creditLimitNotifyPercentages", "smsNotifySettingInfos", "tenure", "otherRelaAccts"
        ]
        for key in subscriber_fields_order:
            if key in subscriber_info_fields:
                if key == "customerId":
                    subscriber_info.append(ET.Comment(f"<bas:customerId>{subscriber_info_fields['customerId']}</bas:customerId>"))
                elif key == "defaultAcctId":
                    subscriber_info.append(ET.Comment(f"<bas:defaultAcctId>{subscriber_info_fields['defaultAcctId']}</bas:defaultAcctId>"))
                elif key == "creditLimitNotifyPercentages":
                    for p in subscriber_info_fields["creditLimitNotifyPercentages"]:
                        ET.SubElement(subscriber_info, "bas:creditLimitNotifyPercentages").text = p
                elif key == "smsNotifySettingInfos":
                    for sms in subscriber_info_fields["smsNotifySettingInfos"]:
                        sms_comment = ET.Comment(f"<bas:smsNotifySettingInfos><bas:eventType>{sms['eventType']}</bas:eventType><bas:openFlag>{sms['openFlag']}</bas:openFlag></bas:smsNotifySettingInfos>")
                        subscriber_info.append(sms_comment)
                elif key == "otherRelaAccts":
                    for rel in subscriber_info_fields["otherRelaAccts"]:
                        rela_acct = ET.SubElement(subscriber_info, "bas:otherRelaAccts")
                        for rel_key, rel_value in rel.items():
                            ET.SubElement(rela_acct, f"bas:{rel_key}").text = rel_value
                else:
                    ET.SubElement(subscriber_info, f"bas:{key}").text = subscriber_info_fields[key]
        
        primary_offer = ET.SubElement(new_subscriber, "bas:primaryOfferInfo")
        ET.SubElement(primary_offer, "bas:offerId").text = data["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["primaryOfferInfo"]["offerId"]
    
    # Transaction Common Info
    transaction_info = ET.SubElement(create_request, "sch:transactionCommonInfo")
    for key, value in data_sets[0]["transactionCommonInfo"].items():
        ET.SubElement(transaction_info, f"bas:{key}").text = value
    
    # Convert to string
    rough_string = ET.tostring(envelope, encoding='unicode')
    parsed = minidom.parseString(rough_string)
    pretty_xml = parsed.toprettyxml(indent="    ", encoding="UTF-8").decode("UTF-8")
    return pretty_xml

# Offer categories mapping
offer_categories = {
    "411155": "Prepaid",
    "411156": "Prepaid",
    "101045": "Prepaid",
    "411158": "Prepaid",
    "215105": "Prepaid",
    "87964": "Prepaid",
    "108879": "Prepaid",
    "175179": "Prepaid",
    "411161": "Prepaid",
    "214292": "Postpaid",
    "96181": "Postpaid",
    "96180": "Postpaid",
    "144882": "Postpaid",
    "167034": "Postpaid",
    "118888": "Postpaid",
    "437101": "Postpaid"    
}

# Offer ID to name mapping for selectbox
offer_id_to_name = {
    "411155": "CelcomDigi Prepaid 5G Kuning (A01)",
    "411156": "CelcomDigi Prepaid 5G Kuning (A02)",
    "101045": "Digi Prepaid LiVE",
    "411158": "Raja Kombo 5G (A01)",
    "215105": "Digi Prepaid NEXT",
    "87964": "DiGi Best Prepaid v4",
    "108879": "Digi Home Broadband",
    "175179": "TONE WOW",
    "411161": "Raja Kombo 5G (A02)",
    "214292": "CelcomDigi Postpaid 5G 60 XV",
    "96181": "E-Reload Postpaid Plan_Agent",
    "96180": "E-Reload Postpaid Plan_Master",
    "144882": "Go Digi 78",
    "167034": "Broadband Monthly 105",
    "118888": "Biz Handy",
    "437101": "CelcomDigi ONE Home Wireless 5G",
}

# Streamlit app
st.markdown('<div class="app-container">', unsafe_allow_html=True)
st.markdown('<div class="header">CRM 3.3 Staging Test Data Creation Tools</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Please start creation between 10:00 AM - 5:30 PM only on Weekday. </div>', unsafe_allow_html=True)

# User name input (simulating modal)
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if not st.session_state.user_name:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("user_name_form"):
            st.markdown('<div class="section-title">Welcome! Let’s Get Started</div>', unsafe_allow_html=True)
            user_name = st.text_input("Enter Your Name", placeholder="Your name", key="user_name_input")
            submit = st.form_submit_button("Start Creating", use_container_width=True)
            if submit:
                if user_name.strip():
                    st.session_state.user_name = user_name.strip()
                    st.rerun()
                else:
                    st.error("Please enter a name to continue.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # Header with user greeting and reset button
    st.markdown('<div class="welcome-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<span class="welcome-text">Hello, {st.session_state.user_name}! 👋</span>', unsafe_allow_html=True)
    with col2:
        if st.button("Reset Session", key="reset_button", help="Reset all inputs and start over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar for global settings
    with st.sidebar:
        st.markdown('<div class="sidebar-title">Settings</div>', unsafe_allow_html=True)
        is_prepaid = st.checkbox("Tick for Prepaid Data Sets (Max 5)\nUntick for Postpaid Data Sets (Max 10)", value=True, key="is_prepaid")
        max_data_sets = 5 if is_prepaid else 10
        st.session_state.max_data_sets = max_data_sets  # Store max_data_sets in session state
        telecom_type = st.selectbox(
            "Telecom Type",
            options=["33 - Mobile Voice", "34 - Broadband"],
            format_func=lambda x: x,
            key="telecom_type"
        )
        telecom_type_value = telecom_type.split(" - ")[0]
        end_row_options = list(range(1, max_data_sets + 1))
        end_row = st.selectbox(
            f"Number of Data Sets (max {max_data_sets})",
            options=end_row_options,
            index=0,
            key="end_row"
        )

    # Main content with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📱 MSISDN/ICCID",
        "⚙️ Configuration",
        "✍️ Data Input",
        "📄 SOAP XML",
        "🔍 Additional Queries"
    ])

    # Tab 1: MSISDN and ICCID Retrieval
    with tab1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Step 1: Retrieve MSISDN and ICCID</div>', unsafe_allow_html=True)
            col3, col4 = st.columns([1, 1])
            with col3:
                if st.button("Get MSISDN", key="get_msisdn", use_container_width=True):
                    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sch="http://oss.huawei.com/webservice/external/services/schema" xmlns:bas="http://oss.huawei.com/webservice/external/services/basetype/">
<soapenv:Header/>
<soapenv:Body>
<sch:getPhoneNumbers>
<sch:AccessSessionRequest>
<bas:accessChannel>10805</bas:accessChannel>
<bas:operatorCode>CSG</bas:operatorCode>
<bas:password>PkzVHH0odLylDCRIPJM+Mw==</bas:password>
<bas:transactionId>202504122319934778</bas:transactionId>
</sch:AccessSessionRequest>
<sch:GetPhoneNumbersRequest>
<sch:QueryCondition>
<sch:deptId>Common</sch:deptId>
<sch:area>1</sch:area>
<sch:matchCode>601%</sch:matchCode>
<sch:msisdnLevel>0</sch:msisdnLevel>
<sch:paidFlag>1</sch:paidFlag>
<sch:telecomType>{telecom_type_value}</sch:telecomType>
<sch:subscriberType>1</sch:subscriberType>
<sch:startRow>1</sch:startRow>
<sch:endRow>{end_row}</sch:endRow>
<sch:lockFlag>0</sch:lockFlag>
</sch:QueryCondition>
</sch:GetPhoneNumbersRequest>
</sch:getPhoneNumbers>
</soapenv:Body>
</soapenv:Envelope>"""
                    st.text_area("MSISDN XML", xml, height=200, key="msisdn_xml")
                    st.session_state.show_msisdn_input = True
                    st.success("✔ Run this in SoapUI")
            
            if st.session_state.get("show_msisdn_input", False):
                msisdn_output = st.text_area("Paste MSISDN Output Here", height=150, key="msisdn_output")
                if msisdn_output:
                    msisdns = parse_msisdn_output(msisdn_output)
                    if msisdns:
                        st.session_state.msisdns = msisdns
                        st.success(f"Extracted {len(msisdns)} MSISDNs. They will be auto-filled in the Data Input tab.")

            with col4:
                if st.button("Get ICCID", key="get_iccid", use_container_width=True):
                    sql = """SELECT ICCID, IMSI, RES_STATUS_ID 
FROM INVENTORY.RES_SIM
WHERE RES_STATUS_ID LIKE '2' AND IS_BIND = '0' AND DEPT_ID ='300' AND BE_ID = '102' ORDER BY ICCID DESC;"""
                    st.text_area("ICCID SQL", sql, height=100, key="iccid_sql")
                    st.session_state.show_iccid_input = True
                    st.success("✔ Run this in SQL")
            
            if st.session_state.get("show_iccid_input", False):
                iccid_output = st.text_area("Paste ICCID Output Here", height=150, key="iccid_output")
                if iccid_output:
                    iccid_imsi_data = parse_iccid_imsi_output(iccid_output)
                    if iccid_imsi_data:
                        st.session_state.iccid_imsi_data = iccid_imsi_data
                        st.success(f"Extracted {len(iccid_imsi_data)} ICCID/IMSI pairs. They will be auto-filled in the Data Input tab.")

            st.markdown('</div>', unsafe_allow_html=True)

    # Tab 2: Configuration
    with tab2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Step 2: Configure Data Sets</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-text">Number of Data Sets Selected: <strong>{end_row}</strong> (Max: {max_data_sets})</div>', unsafe_allow_html=True)
            
            # Plan selection for multiple data sets
            plan_option = None
            if end_row > 1:
                prepaid_plan_options = [
                    ("ALL_411155", "ALL CelcomDigi Prepaid 5G Kuning (A01)"),
                    ("ALL_411156", "ALL CelcomDigi Prepaid 5G Kuning (A02)"),
                    ("ALL_215105", "ALL Digi Prepaid NEXT"),
                    ("ALL_87964", "ALL DiGi Best Prepaid v4"),
                    ("ALL_108879", "ALL Digi Home Broadband"),
                    ("ALL_175179", "ALL TONE WOW"),
                    ("ALL_411161", "ALL Raja Kombo 5G (A02)"),
                    ("MIX_3_411155_2_411156", "MIX 3 CelcomDigi Prepaid 5G Kuning (A01) & 2 CelcomDigi Prepaid 5G Kuning (A02)")
                ]
                postpaid_plan_options = [
                    ("ALL_214292", "ALL CelcomDigi Postpaid 5G 60 XV"),
                    ("ALL_96181", "ALL E-Reload Postpaid Plan_Agent"),
                    ("ALL_96180", "ALL E-Reload Postpaid Plan_Master"),
                    ("ALL_144882", "ALL Go Digi 78"),
                    ("ALL_167034", "ALL Broadband Monthly 105"),
                    ("ALL_118888", "ALL Biz Handy"),
                    ("437101", "ALL CelcomDigi ONE Home Wireless 5G"),
                    ("MIX_5_214292_5_96181_5_96180_5_144882", "MIX 5 CelcomDigi Postpaid 5G 60 XV, 5 E-Reload Postpaid Plan_Agent, 5 E-Reload Postpaid Plan_Master, 5 Go Digi 78"),
                    ("MIX_10_96181_10_96180", "MIX 10 E-Reload Postpaid Plan_Agent, 10 E-Reload Postpaid Plan_Master"),
                    ("MIX_10_214292_10_144882", "MIX 10 CelcomDigi Postpaid 5G 60 XV, 10 Go Digi 78")
                ]
                plan_options = prepaid_plan_options if is_prepaid else postpaid_plan_options
                plan_option = st.selectbox(
                    "Select Plan for Data Sets",
                    options=plan_options,
                    format_func=lambda x: x[1],
                    key="plan_option"
                )[0]

            if st.button("Generate Input Form", key="generate_form", use_container_width=True):
                st.session_state.generated_data_sets_count = end_row
                st.session_state.data_sets = [generate_dummy_data(i + 1) for i in range(end_row)]
                
                # Auto-fill MSISDN, ICCID, IMSI, Telecom Type, and Offer ID
                msisdns = st.session_state.get("msisdns", [])
                iccid_imsi_data = st.session_state.get("iccid_imsi_data", [])
                
                # Define Offer ID assignments based on plan_option
                offer_ids = [""] * end_row
                if end_row > 1 and plan_option:
                    if is_prepaid:
                        if plan_option == "ALL_411155":
                            offer_ids = ["411155"] * end_row
                        elif plan_option == "ALL_411156":
                            offer_ids = ["411156"] * end_row
                        elif plan_option == "ALL_215105":
                            offer_ids = ["215105"] * end_row
                        elif plan_option == "ALL_87964":
                            offer_ids = ["87964"] * end_row
                        elif plan_option == "ALL_108879":
                            offer_ids = ["108879"] * end_row
                        elif plan_option == "ALL_411161":
                            offer_ids = ["411161"] * end_row
                        elif plan_option == "ALL_175179":
                            offer_ids = ["175179"] * end_row    
                        elif plan_option == "MIX_3_411155_2_411156":
                            offer_ids = ["411155"] * min(3, end_row) + ["411156"] * (end_row - min(3, end_row))
                    else:
                        if plan_option == "ALL_214292":
                            offer_ids = ["214292"] * end_row
                        elif plan_option == "ALL_96181":
                            offer_ids = ["96181"] * end_row
                        elif plan_option == "ALL_96180":
                            offer_ids = ["96180"] * end_row   
                        elif plan_option == "ALL_144882":
                            offer_ids = ["144882"] * end_row
                        elif plan_option == "ALL_167034":
                            offer_ids = ["167034"] * end_row
                        elif plan_option == "ALL_118888":
                            offer_ids = ["118888"] * end_row
                        elif plan_option == "ALL_437101":
                            offer_ids = ["437101"] * end_row    
                        elif plan_option == "MIX_5_214292_5_96181_5_96180_5_144882":
                            sets_per_plan = min(5, end_row // 4 + (1 if end_row % 4 > 0 else 0))
                            remaining = end_row
                            offer_ids = (
                                ["214292"] * min(sets_per_plan, remaining) +
                                ["96181"] * min(sets_per_plan, max(0, remaining - sets_per_plan)) +
                                ["96180"] * min(sets_per_plan, max(0, remaining - 2 * sets_per_plan)) +
                                ["144882"] * max(0, remaining - 3 * sets_per_plan)
                            )
                        elif plan_option == "MIX_10_96181_10_96180":
                            sets_per_plan = min(10, end_row // 2 + (1 if end_row % 2 > 0 else 0))
                            remaining = end_row
                            offer_ids = (
                                ["96181"] * min(sets_per_plan, remaining) +
                                ["96180"] * max(0, remaining - sets_per_plan)
                            )
                        elif plan_option == "MIX_10_214292_10_144882":
                            sets_per_plan = min(10, end_row // 2 + (1 if end_row % 2 > 0 else 0))
                            remaining = end_row
                            offer_ids = (
                                ["214292"] * min(sets_per_plan, remaining) +
                                ["144882"] * max(0, remaining - sets_per_plan)
                            )

                for i in range(end_row):
                    # Auto-fill MSISDN
                    if i < len(msisdns):
                        st.session_state[f"msisdn_{i}"] = msisdns[i]
                    else:
                        st.session_state[f"msisdn_{i}"] = ""
                    
                    # Auto-fill ICCID and IMSI
                    if i < len(iccid_imsi_data):
                        st.session_state[f"iccid_{i}"] = iccid_imsi_data[i]["iccid"]
                        st.session_state[f"imsi_{i}"] = iccid_imsi_data[i]["imsi"]
                    else:
                        st.session_state[f"iccid_{i}"] = ""
                        st.session_state[f"imsi_{i}"] = ""
                    
                    # Set default Telecom Type from sidebar
                    st.session_state[f"telecomType_{i}"] = telecom_type
                    
                    # Set Offer ID based on plan_option
                    offer_id = offer_ids[i]
                    offer_name = offer_id_to_name.get(offer_id, "Select an Offer")
                    st.session_state[f"offerId_{i}"] = (offer_id, offer_name)
                
                st.success("Input form generated! Proceed to the Data Input tab.")
            st.markdown('</div>', unsafe_allow_html=True)

    # Tab 3: Data Input
    with tab3:
        if "generated_data_sets_count" in st.session_state:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Step 3: Enter Data for Each Set</div>', unsafe_allow_html=True)
                data_sets = st.session_state.data_sets
                for i in range(st.session_state.generated_data_sets_count):
                    st.markdown(f'<div class="data-set-title">Data Set {i + 1}</div>', unsafe_allow_html=True)
                    col_msisdn, col_iccid, col_imsi = st.columns(3)
                    with col_msisdn:
                        st.markdown('<span class="label">MSISDN <span class="required">*</span></span>', unsafe_allow_html=True)
                        msisdn = st.text_input("", value=st.session_state.get(f"msisdn_{i}", ""), placeholder="e.g., 601002033200", key=f"msisdn_{i}")
                    with col_iccid:
                        st.markdown('<span class="label">ICCID <span class="required">*</span></span>', unsafe_allow_html=True)
                        iccid = st.text_input("", value=st.session_state.get(f"iccid_{i}", ""), placeholder="e.g., 89601619041600000091", key=f"iccid_{i}")
                    with col_imsi:
                        st.markdown('<span class="label">IMSI <span class="required">*</span></span>', unsafe_allow_html=True)
                        imsi = st.text_input("", value=st.session_state.get(f"imsi_{i}", ""), placeholder="e.g., 502161082020265", key=f"imsi_{i}")
                    col_telecom, col_offer = st.columns(2)
                    with col_telecom:
                        st.markdown('<span class="label">Telecom Type <span class="required">*</span></span>', unsafe_allow_html=True)
                        telecom_type_input = st.selectbox(
                            "",
                            options=["", "33 - Mobile Voice", "34 - Broadband"],
                            index=["", "33 - Mobile Voice", "34 - Broadband"].index(st.session_state.get(f"telecomType_{i}", telecom_type)),
                            format_func=lambda x: x if x else "Select Telecom Type",
                            key=f"telecomType_{i}"
                        )
                    with col_offer:
                        st.markdown('<span class="label">Offer ID <span class="required">*</span></span>', unsafe_allow_html=True)
                        offer_options = [
                            ("", "Select an Offer"),
                            ("411155", "CelcomDigi Prepaid 5G Kuning (A01)"),
                            ("411156", "CelcomDigi Prepaid 5G Kuning (A02)"),
                            ("101045", "Digi Prepaid LiVE"),
                            ("411158", "Raja Kombo 5G (A01)"),
                            ("215105", "Digi Prepaid NEXT"),
                            ("87964", "DiGi Best Prepaid v4"),
                            ("108879", "Digi Home Broadband"),
                            ("175179", "TONE WOW"),
                            ("411161", "Raja Kombo 5G (A02)"),
                            ("214292", "CelcomDigi Postpaid 5G 60 XV"),
                            ("96181", "E-Reload Postpaid Plan_Agent"),
                            ("96180", "E-Reload Postpaid Plan_Master"),
                            ("144882", "Go Digi 78"),
                            ("118888", "Biz Handy"),
                            ("437101", "CelcomDigi ONE Home Wireless 5G"),
                            ("167034","Broadband Monthly 105")
                        ]
                        # Filter offer options based on Prepaid/Postpaid selection
                        if is_prepaid:
                            offer_options = [(oid, name) for oid, name in offer_options if oid == "" or offer_categories.get(oid) == "Prepaid"]
                        else:
                            offer_options = [(oid, name) for oid, name in offer_options if oid == "" or offer_categories.get(oid) == "Postpaid"]
                        # Get the stored Offer ID tuple, default to ("", "Select an Offer") if not set
                        stored_offer = st.session_state.get(f"offerId_{i}", ("", "Select an Offer"))
                        # Find the index of the stored offer in offer_options, default to 0 if not found
                        try:
                            offer_index = [(oid, name) for oid, name in offer_options].index(stored_offer)
                        except ValueError:
                            offer_index = 0
                        offer_id = st.selectbox(
                            "",
                            options=offer_options,
                            format_func=lambda x: x[1],
                            index=offer_index,
                            key=f"offerId_{i}"
                        )
                    col_converge, col_paid = st.columns(2)
                    offer_id_value = offer_id[0]
                    converge_flag = "0" if offer_id_value and offer_categories.get(offer_id_value) == "Prepaid" else "1" if offer_id_value else ""
                    paid_flag = converge_flag
                    with col_converge:
                        st.markdown('<span class="label">Converge Flag</span>', unsafe_allow_html=True)
                        st.selectbox(
                            "",
                            options=["", "0 - Prepaid", "1 - Postpaid"],
                            index=["", "0 - Prepaid", "1 - Postpaid"].index(f"{converge_flag} - {'Prepaid' if converge_flag == '0' else 'Postpaid'}" if converge_flag else ""),
                            format_func=lambda x: x if x else "Select Converge Flag",
                            disabled=True,
                            key=f"converge_flag_{i}"
                        )
                    with col_paid:
                        st.markdown('<span class="label">Paid Flag</span>', unsafe_allow_html=True)
                        st.selectbox(
                            "",
                            options=["", "0 - Prepaid", "1 - Postpaid"],
                            index=["", "0 - Prepaid", "1 - Postpaid"].index(f"{paid_flag} - {'Prepaid' if paid_flag == '0' else 'Postpaid'}" if paid_flag else ""),
                            format_func=lambda x: x if x else "Select Paid Flag",
                            disabled=True,
                            key=f"paidFlag_{i}"
                        )

                # Collapsible sections for advanced settings
                st.markdown('<div class="advanced-settings">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Advanced Settings</div>', unsafe_allow_html=True)
                sections = [
                    {"name": "AccessSessionRequest", "fields": data_sets[0]["accessSessionRequest"]},
                    {
                        "name": "customerInfo",
                        "fields": {
                            k: v for k, v in data_sets[0]["customerInfo"].items()
                            if k not in ["customerSegment", "createDate", "customerAddressInfos", "customerRelationInfos", "corporationInfo"] and isinstance(v, str)
                        }
                    },
                    {"name": "transactionCommonInfo", "fields": data_sets[0]["transactionCommonInfo"]}
                ]
                for section in sections:
                    with st.expander(section["name"], expanded=False):
                        for key, value in section["fields"].items():
                            # Special handling for subscriberType to make it clear and user-friendly
                            if key == "subscriberType":
                                st.text_input(
                                    "Subscriber Type",
                                    value=st.session_state.get(f"customerInfo_subscriberType", value),
                                    placeholder="e.g., 1-Mass, 6-Corporate",
                                    key=f"customerInfo_subscriberType"
                                )
                            else:
                                st.text_input(
                                    key,
                                    value=st.session_state.get(f"{section['name']}_{key}", value),
                                    key=f"{section['name']}_{key}"
                                )
                st.markdown('</div>', unsafe_allow_html=True)

                # Generate SOAP XML button
                if st.button("Generate SOAP XML", key="generate_soap", use_container_width=True):
                    with st.spinner("Generating SOAP XML..."):
                        try:
                            # Sanitize data_sets
                            if not isinstance(st.session_state.get("data_sets"), list) or len(st.session_state.data_sets) > max_data_sets:
                                st.warning("Invalid data_sets in session state. Reinitializing.")
                                st.session_state.generated_data_sets_count = min(st.session_state.get("generated_data_sets_count", 1), max_data_sets)
                                st.session_state.data_sets = [generate_dummy_data(i + 1) for i in range(st.session_state.generated_data_sets_count)]
                            data_sets = st.session_state.data_sets
                
                            # Validate customerInfo structure
                            expected_customer_info_keys = [
                                "customerId", "customerFlag", "subscriberType", "customerCode", "idType", "idNumber",
                                "expiryDateofcertificate", "title", "firstName", "middleName", "lastName",
                                "nationality", "customerLang", "customerLevel", "customerGroup", "race",
                                "occupation", "customerDateofBirth", "customerGender", "maritalStatus",
                                "customerStatus", "numOfSubPerCondition", "info1", "info2", "info3",
                                "info4", "info5", "customerAddressInfos", "customerRelationInfos", "corporationInfo"
                            ]
                            nested_keys = ["customerAddressInfos", "customerRelationInfos", "corporationInfo"]
                            for i in range(len(data_sets)):
                                customer_info = data_sets[i]["customerInfo"]
                                if sorted(customer_info.keys()) != sorted(expected_customer_info_keys):
                                    st.warning(f"Invalid keys in data_sets[{i}]['customerInfo']. Reinitializing data_sets.")
                                    st.session_state.data_sets = [generate_dummy_data(j + 1) for j in range(st.session_state.generated_data_sets_count)]
                                    data_sets = st.session_state.data_sets
                                    break
                                for key, value in customer_info.items():
                                    if key not in nested_keys and not isinstance(value, str):
                                        st.warning(f"Invalid value type for {key} in data_sets[{i}]['customerInfo']. Reinitializing data_sets.")
                                        st.session_state.data_sets = [generate_dummy_data(j + 1) for j in range(st.session_state.generated_data_sets_count)]
                                        data_sets = st.session_state.data_sets
                                        break
                
                            # Update data sets
                            for i in range(st.session_state.generated_data_sets_count):
                                # Validate inputs
                                msisdn = st.session_state.get(f"msisdn_{i}", "")
                                iccid = st.session_state.get(f"iccid_{i}", "")
                                imsi = st.session_state.get(f"imsi_{i}", "")
                                telecom_type_input = st.session_state.get(f"telecomType_{i}", telecom_type)
                                valid_telecom_options = ["", "33 - Mobile Voice", "34 - Broadband"]
                                if telecom_type_input not in valid_telecom_options:
                                    st.warning(f"Invalid Telecom Type for Data Set {i + 1}. Resetting to default.")
                                    telecom_type_input = telecom_type
                                    st.session_state[f"telecomType_{i}"] = telecom_type
                                telecom_type_value = telecom_type_input.split(" - ")[0] if telecom_type_input else ""
                                raw_offer_id = st.session_state.get(f"offerId_{i}", ("", ""))
                                if not isinstance(raw_offer_id, tuple) or len(raw_offer_id) != 2:
                                    raise ValueError(f"Expected a 2-element tuple for offerId_{i}, got {raw_offer_id}")
                                offer_id = raw_offer_id[0]
                
                                if not msisdn or not msisdn.isdigit() or not (10 <= len(msisdn) <= 12):
                                    st.error(f"Invalid MSISDN for Data Set {i + 1}. Must be 10-12 digits.")
                                    break
                                if not iccid or not iccid.isdigit() or not (19 <= len(iccid) <= 20):
                                    st.error(f"Invalid ICCID for Data Set {i + 1}. Must be 19-20 digits.")
                                    break
                                if not imsi or not imsi.isdigit() or len(imsi) != 15:
                                    st.error(f"Invalid IMSI for Data Set {i + 1}. Must be 15 digits.")
                                    break
                                if not telecom_type_value:
                                    st.error(f"Please select a Telecom Type for Data Set {i + 1}.")
                                    break
                                if not offer_id:
                                    st.error(f"Please select an Offer ID for Data Set {i + 1}.")
                                    break
                                if offer_id not in offer_categories:
                                    st.error(f"Invalid Offer ID {offer_id} for Data Set {i + 1}.")
                                    break
                                if is_prepaid and offer_categories[offer_id] != "Prepaid":
                                    st.error(f"Selected Offer ID {offer_id} is not a Prepaid offer for Data Set {i + 1}.")
                                    break
                                if not is_prepaid and offer_categories[offer_id] != "Postpaid":
                                    st.error(f"Selected Offer ID {offer_id} is not a Postpaid offer for Data Set {i + 1}.")
                                    break
                
                                is_prepaid_offer = offer_categories[offer_id] == "Prepaid"
                                converge_flag = "0" if is_prepaid_offer else "1"
                                paid_flag = converge_flag
                
                                valid_flag_options = ["", "0 - Prepaid", "1 - Postpaid"]
                                current_converge_flag = st.session_state.get(f"converge_flag_{i}", "")
                                current_paid_flag = st.session_state.get(f"paidFlag_{i}", "")
                                if current_converge_flag not in valid_flag_options:
                                    st.session_state[f"converge_flag_{i}"] = f"{converge_flag} - {'Prepaid' if converge_flag == '0' else 'Postpaid'}"
                                if current_paid_flag not in valid_flag_options:
                                    st.session_state[f"paidFlag_{i}"] = f"{paid_flag} - {'Prepaid' if paid_flag == '0' else 'Postpaid'}"
                
                                # Update customerInfo fields from Advanced Settings first
                                customer_info_fields = {
                                    k: v for k, v in data_sets[i]["customerInfo"].items()
                                    if k not in nested_keys
                                }
                                for key in customer_info_fields:
                                    if isinstance(data_sets[i]["customerInfo"][key], str):
                                        session_key = f"customerInfo_{key}"
                                        if session_key in st.session_state:
                                            data_sets[i]["customerInfo"][key] = st.session_state[session_key]
                
                                # Update newAcctSubscriberInfos fields
                                data_sets[i]["newAcctSubscriberInfos"][0]["accountInfo"]["converge_flag"] = converge_flag
                                data_sets[i]["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberInfo"]["paidFlag"] = paid_flag
                                data_sets[i]["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberInfo"]["msisdn"] = msisdn
                                data_sets[i]["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberInfo"]["iccid"] = iccid
                                data_sets[i]["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberInfo"]["imsi"] = imsi
                                data_sets[i]["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberInfo"]["telecomType"] = telecom_type_value
                                data_sets[i]["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["primaryOfferInfo"]["offerId"] = offer_id
                                # Update subscriberType in subscriberInfo to match customerInfo
                                data_sets[i]["newAcctSubscriberInfos"][0]["newSubscriberInfos"]["subscriberInfo"]["subscriberType"] = data_sets[i]["customerInfo"]["subscriberType"]
                
                            # Update AccessSessionRequest fields
                            access_channel = st.session_state.get("AccessSessionRequest_accessChannel", "10050")
                            data_sets[0]["accessSessionRequest"]["accessChannel"] = access_channel
                
                            # Update transactionCommonInfo remark
                            remark = st.session_state.get("transactionCommonInfo_remark", "")
                            remark = remark.lstrip("TEST-").strip() if remark else random_string(4)
                            remark_value = f"TEST-{remark}"
                            if st.session_state.user_name:
                                remark_value += f"CRQ{st.session_state.user_name}"
                            for data in data_sets:
                                data["transactionCommonInfo"]["remark"] = remark_value
                
                            # Generate XML
                            xml = generate_soap_xml(data_sets)
                            st.session_state.output_xml = xml
                            st.success("SOAP XML generated successfully! Check the SOAP XML tab.")
                        except Exception as e:
                            st.error(f"Failed to generate SOAP XML: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Step 3: Enter Data for Each Set</div>', unsafe_allow_html=True)
                st.markdown('<div class="info-text">Please generate the input form in the Configuration tab first.</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # Tab 4: SOAP XML
    with tab4:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Step 4: View Generated SOAP XML</div>', unsafe_allow_html=True)
            if "output_xml" in st.session_state:
                st.text_area("Generated SOAP XML", st.session_state.output_xml, height=300, key="output_xml")
                st.success("✔ Run this in SoapUI")
            else:
                st.markdown('<div class="info-text">Generate the SOAP XML in the Data Input tab to view it here.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Tab 5: Additional Queries
    with tab5:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Step 5: Run Additional Queries</div>', unsafe_allow_html=True)
            msisdns = []
            if "generated_data_sets_count" in st.session_state:
                for i in range(st.session_state.generated_data_sets_count):
                    msisdn = st.session_state.get(f"msisdn_{i}", "")
                    if msisdn and msisdn.isdigit() and 10 <= len(msisdn) <= 12 and msisdn.startswith("60"):
                        msisdn = msisdn[2:]
                        msisdns.append(msisdn)
            msisdn_list = ", ".join(f"'{msisdn}'" for msisdn in msisdns) if msisdns else "'MSISDNHERE'"
            
            col5, col6 = st.columns([1, 1])
            with col5:
                if st.button("Check Number Status", key="check_status", use_container_width=True):
                    sql = f"""--Check taken number status
select MSISDN, RES_STATUS_ID from INVENTORY.RES_MSISDN where MSISDN in ({msisdn_list});"""
                    st.text_area("Check Number Status SQL", sql, height=100, key="check_status_sql")
                    st.success("✔ Run this in SQL")
            with col6:
                if st.button("Run PBO Query", key="pbo_query", use_container_width=True):
                    sql = f"""select t.*, t.rowid from ccare.inf_businessinfo t where t.msisdn in ({msisdn_list});"""
                    st.text_area("PBO SQL", sql, height=100, key="pbo_sql")
                    st.success("✔ Run this in SQL")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
