from flask import Flask, jsonify, render_template, request, redirect
from app import app
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads
import os
import dialogflow
import requests
import json
import pusher

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/shantanu/Documents/hackAD18/app/Movie-Bot-*.json"

app.config["MONGO_URI"] = "mongodb://localhost:27017/hackAD"
mongo = PyMongo(app)

client = MongoClient()

all_countries = {
	'AF': 'AFGHANISTAN',
	'AX': 'ALAND ISLANDS',
	'AL': 'ALBANIA',
	'DZ': 'ALGERIA',
	'AS': 'AMERICAN SAMOA',
	'AD': 'ANDORRA',
	'AO': 'ANGOLA',
	'AI': 'ANGUILLA',
	'AQ': 'ANTARCTICA',
	'AG': 'ANTIGUA AND BARBUDA',
	'AR': 'ARGENTINA',
	'AM': 'ARMENIA',
	'AW': 'ARUBA',
	'AU': 'AUSTRALIA',
	'AT': 'AUSTRIA',
	'AZ': 'AZERBAIJAN',
	'BS': 'BAHAMAS',
	'BH': 'BAHRAIN',
	'BD': 'BANGLADESH',
	'BB': 'BARBADOS',
	'BY': 'BELARUS',
	'BE': 'BELGIUM',
	'BZ': 'BELIZE',
	'BJ': 'BENIN',
	'BM': 'BERMUDA',
	'BT': 'BHUTAN',
	'BO': 'BOLIVIA, PLURINATIONAL STATE OF',
	'BQ': 'BONAIRE, SINT EUSTATIUS AND SABA',
	'BA': 'BOSNIA AND HERZEGOVINA',
	'BW': 'BOTSWANA',
	'BV': 'BOUVET ISLAND',
	'BR': 'BRAZIL',
	'IO': 'BRITISH INDIAN OCEAN TERRITORY',
	'BN': 'BRUNEI DARUSSALAM',
	'BG': 'BULGARIA',
	'BF': 'BURKINA FASO',
	'BI': 'BURUNDI',
	'KH': 'CAMBODIA',
	'CM': 'CAMEROON',
	'CA': 'CANADA',
	'CV': 'CAPE VERDE',
	'KY': 'CAYMAN ISLANDS',
	'CF': 'CENTRAL AFRICAN REPUBLIC',
	'TD': 'CHAD',
	'CL': 'CHILE',
	'CN': 'CHINA',
	'CX': 'CHRISTMAS ISLAND',
	'CC': 'COCOS (KEELING) ISLANDS',
	'CO': 'COLOMBIA',
	'KM': 'COMOROS',
	'CG': 'CONGO',
	'CD': 'CONGO, THE DEMOCRATIC REPUBLIC OF THE',
	'CK': 'COOK ISLANDS',
	'CR': 'COSTA RICA',
	'CI': 'CoTE D\'IVOIRE',
	'HR': 'CROATIA',
	'CU': 'CUBA',
	'CW': 'CURACAO',
	'CY': 'CYPRUS',
	'CZ': 'CZECH REPUBLIC',
	'DK': 'DENMARK',
	'DJ': 'DJIBOUTI',
	'DM': 'DOMINICA',
	'DO': 'DOMINICAN REPUBLIC',
	'EC': 'ECUADOR',
	'EG': 'EGYPT',
	'SV': 'EL SALVADOR',
	'GQ': 'EQUATORIAL GUINEA',
	'ER': 'ERITREA',
	'EE': 'ESTONIA',
	'ET': 'ETHIOPIA',
	'FK': 'FALKLAND ISLANDS (MALVINAS)',
	'FO': 'FAROE ISLANDS',
	'FJ': 'FIJI',
	'FI': 'FINLAND',
	'FR': 'FRANCE',
	'GF': 'FRENCH GUIANA',
	'PF': 'FRENCH POLYNESIA',
	'TF': 'FRENCH SOUTHERN TERRITORIES',
	'GA': 'GABON',
	'GM': 'GAMBIA',
	'GE': 'GEORGIA',
	'DE': 'GERMANY',
	'GH': 'GHANA',
	'GI': 'GIBRALTAR',
	'GR': 'GREECE',
	'GL': 'GREENLAND',
	'GD': 'GRENADA',
	'GP': 'GUADELOUPE',
	'GU': 'GUAM',
	'GT': 'GUATEMALA',
	'GG': 'GUERNSEY',
	'GN': 'GUINEA',
	'GW': 'GUINEA-BISSAU',
	'GY': 'GUYANA',
	'HT': 'HAITI',
	'HM': 'HEARD ISLAND AND MCDONALD ISLANDS',
	'VA': 'HOLY SEE (VATICAN CITY STATE)',
	'HN': 'HONDURAS',
	'HK': 'HONG KONG',
	'HU': 'HUNGARY',
	'IS': 'ICELAND',
	'IN': 'INDIA',
	'ID': 'INDONESIA',
	'IR': 'IRAN, ISLAMIC REPUBLIC OF',
	'IQ': 'IRAQ',
	'IE': 'IRELAND',
	'IM': 'ISLE OF MAN',
	'IL': 'ISRAEL',
	'IT': 'ITALY',
	'JM': 'JAMAICA',
	'JP': 'JAPAN',
	'JE': 'JERSEY',
	'JO': 'JORDAN',
	'KZ': 'KAZAKHSTAN',
	'KE': 'KENYA',
	'KI': 'KIRIBATI',
	'KP': 'KOREA, DEMOCRATIC PEOPLE\'S REPUBLIC OF',
	'KR': 'KOREA, REPUBLIC OF',
	'KW': 'KUWAIT',
	'KG': 'KYRGYZSTAN',
	'LA': 'LAO PEOPLE\'S DEMOCRATIC REPUBLIC',
	'LV': 'LATVIA',
	'LB': 'LEBANON',
	'LS': 'LESOTHO',
	'LR': 'LIBERIA',
	'LY': 'LIBYAN ARAB JAMAHIRIYA',
	'LI': 'LIECHTENSTEIN',
	'LT': 'LITHUANIA',
	'LU': 'LUXEMBOURG',
	'MO': 'MACAO',
	'MK': 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF',
	'MG': 'MADAGASCAR',
	'MW': 'MALAWI',
	'MY': 'MALAYSIA',
	'MV': 'MALDIVES',
	'ML': 'MALI',
	'MT': 'MALTA',
	'MH': 'MARSHALL ISLANDS',
	'MQ': 'MARTINIQUE',
	'MR': 'MAURITANIA',
	'MU': 'MAURITIUS',
	'YT': 'MAYOTTE',
	'MX': 'MEXICO',
	'FM': 'MICRONESIA, FEDERATED STATES OF',
	'MD': 'MOLDOVA, REPUBLIC OF',
	'MC': 'MONACO',
	'MN': 'MONGOLIA',
	'ME': 'MONTENEGRO',
	'MS': 'MONTSERRAT',
	'MA': 'MOROCCO',
	'MZ': 'MOZAMBIQUE',
	'MM': 'MYANMAR',
	'NA': 'NAMIBIA',
	'NR': 'NAURU',
	'NP': 'NEPAL',
	'NL': 'NETHERLANDS',
	'NC': 'NEW CALEDONIA',
	'NZ': 'NEW ZEALAND',
	'NI': 'NICARAGUA',
	'NE': 'NIGER',
	'NG': 'NIGERIA',
	'NU': 'NIUE',
	'NF': 'NORFOLK ISLAND',
	'MP': 'NORTHERN MARIANA ISLANDS',
	'NO': 'NORWAY',
	'OM': 'OMAN',
	'PK': 'PAKISTAN',
	'PW': 'PALAU',
	'PS': 'PALESTINIAN TERRITORY, OCCUPIED',
	'PA': 'PANAMA',
	'PG': 'PAPUA NEW GUINEA',
	'PY': 'PARAGUAY',
	'PE': 'PERU',
	'PH': 'PHILIPPINES',
	'PN': 'PITCAIRN',
	'PL': 'POLAND',
	'PT': 'PORTUGAL',
	'PR': 'PUERTO RICO',
	'QA': 'QATAR',
	'RE': 'REUNION',
	'RO': 'ROMANIA',
	'RU': 'RUSSIAN FEDERATION',
	'RW': 'RWANDA',
	'BL': 'SAINT BARTHELEMY',
	'SH': 'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA',
	'KN': 'SAINT KITTS AND NEVIS',
	'LC': 'SAINT LUCIA',
	'MF': 'SAINT MARTIN (FRENCH PART)',
	'PM': 'SAINT PIERRE AND MIQUELON',
	'VC': 'SAINT VINCENT AND THE GRENADINES',
	'WS': 'SAMOA',
	'SM': 'SAN MARINO',
	'ST': 'SAO TOME AND PRINCIPE',
	'SA': 'SAUDI ARABIA',
	'SN': 'SENEGAL',
	'RS': 'SERBIA',
	'SC': 'SEYCHELLES',
	'SL': 'SIERRA LEONE',
	'SG': 'SINGAPORE',
	'SX': 'SINT MAARTEN (DUTCH PART)',
	'SK': 'SLOVAKIA',
	'SI': 'SLOVENIA',
	'SB': 'SOLOMON ISLANDS',
	'SO': 'SOMALIA',
	'ZA': 'SOUTH AFRICA',
	'GS': 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS',
	'SS': 'SOUTH SUDAN',
	'ES': 'SPAIN',
	'LK': 'SRI LANKA',
	'SD': 'SUDAN',
	'SR': 'SURINAME',
	'SJ': 'SVALBARD AND JAN MAYEN',
	'SZ': 'SWAZILAND',
	'SE': 'SWEDEN',
	'CH': 'SWITZERLAND',
	'SY': 'SYRIAN ARAB REPUBLIC',
	'TW': 'TAIWAN, PROVINCE OF CHINA',
	'TJ': 'TAJIKISTAN',
	'TZ': 'TANZANIA, UNITED REPUBLIC OF',
	'TH': 'THAILAND',
	'TL': 'TIMOR-LESTE',
	'TG': 'TOGO',
	'TK': 'TOKELAU',
	'TO': 'TONGA',
	'TT': 'TRINIDAD AND TOBAGO',
	'TN': 'TUNISIA',
	'TR': 'TURKEY',
	'TM': 'TURKMENISTAN',
	'TC': 'TURKS AND CAICOS ISLANDS',
	'TV': 'TUVALU',
	'UG': 'UGANDA',
	'UA': 'UKRAINE',
	'AE': 'UNITED ARAB EMIRATES',
	'GB': 'UNITED KINGDOM',
	'US': 'UNITED STATES',
	'UM': 'UNITED STATES MINOR OUTLYING ISLANDS',
	'UY': 'URUGUAY',
	'UZ': 'UZBEKISTAN',
	'VU': 'VANUATU',
	'VE': 'VENEZUELA, BOLIVARIAN REPUBLIC OF',
	'VN': 'VIET NAM',
	'VG': 'VIRGIN ISLANDS, BRITISH',
	'VI': 'VIRGIN ISLANDS, U.S.',
	'WF': 'WALLIS AND FUTUNA',
	'EH': 'WESTERN SAHARA',
	'YE': 'YEMEN',
	'ZM': 'ZAMBIA',
	'ZW': 'ZIMBABWE',}

codes = []
for key in all_countries:
    codes.append(key)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text


db = client.hackAD
collections = db.places
@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():

    input_destination = ""
    input_budget = 0
    input_flights = ""
    input_hotel = ""
    input_visa = ""
    input_advice = ""

    input_destination = str(request.args.get('dest')).upper()
    if request.args.get('money'):
        input_budget = int(request.args.get('money'))
    input_flights = str(request.args.get('flights'))
    input_hotel = str(request.args.get('hotel'))
    input_visa = str(request.args.get('visa'))
    input_advice = str(request.args.get('advice'))
    if input_advice != 'None' and input_destination != 'NONE' and input_budget != 0:
        inserted = collections.insert_one({"country" : input_destination, "budget": input_budget, "flight" : input_flights,"hotel" : input_hotel, "visa" : input_visa, "when_there": input_advice})
        print(inserted)

    print(input_budget, input_destination, input_flights, input_hotel, input_visa, input_advice)

    countries_present = []
    all_docs = collections.find({"country" : {"$exists" : True}}, {"_id" : False})
    for entry in all_docs:
        if entry['country'] in codes:
            countries_present.append(entry['country'])
            codes.remove(entry['country'])

    country = (str(request.args.get('country'))).upper()
    country_selected = False
    if country != 'NONE':
        country_selected = True

    which_break = str(request.args.get('break'))
    budget = 0
    days = 0
    if request.args.get('budget'):
        budget = int(request.args.get('budget'))
    if request.args.get('numberOfDays'):
        days = int(request.args.get('numberOfDays'))

    test = ""
    test = dumps(collections.find({"country" : country}, {"_id" : False}))
    test = loads(test)
    counter = 0
    for_NLP = [entry['when_there'][:150] for entry in test]
    advice_types = []
    for entry in test:
        if entry['budget'] <= budget:
            counter = counter + 1
        message = entry['when_there']
        project_id = 'karu-49941'
        fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
        advice_types.append(fulfillment_text)


    return render_template('index.html', country=country, data = test, budget = budget, countries_db = countries_present, counter = counter, all_countries = all_countries, advice_types = advice_types, country_selected = country_selected )
