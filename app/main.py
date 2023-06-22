import pandas as pd
from flask import Flask, request, jsonify
from unidecode import unidecode
df = pd.read_csv('combined_data_nodiacritic.csv')
app = Flask(__name__)
@app.route('/real_estate_price', methods=['POST'])
def api():   
    data = request.get_json()     
    type_house = data['propertyBasicInfo']['typeOfRealEstate']['value']
    street = data['propertyBasicInfo']['address']['value']['street']
    district = data['propertyBasicInfo']['address']['value']['district']
    landsize = data["propertyBasicInfo"]["landSize"]['value']
    city = data['propertyBasicInfo']['address']['value']['city']
    if any(var is None for var in [landsize, type_house, district, city,street]):
        return jsonify({'error': 'Input cannot be null.'})
    # Trả về JSON với thông báo lỗi
    decoded_city = unidecode(city).lower()
    decoded_district = unidecode(district).lower()
    decoded_street = unidecode(street).lower()
    if decoded_city != ' ha noi':
        return jsonify({'error Api': 'this feature will update soon'})
    if type_house == 'townhouse':
      mask = (df['quận'] == district) & (df['tên đường'] == street)
      if mask.any():
        price = int(df.loc[mask, 'giá đất ở v1'].values[0]) * 1000 * landsize
        return jsonify({'real_estate_price': price})
      else:
        return jsonify({'real_estate_price': 0, 'district': district, 'street': street})
    elif type_house == 'apartment' or type_house == 'miniApartment':
        return jsonify({'real_estate_price': 0, 'district': district, 'street': street})
    else:
        mask = (df['quận'] == district) & (df['tên đường'] == street)
        if mask.any():
         price = int(df.loc[mask, 'giá đất ở v2'].values[0]) * 1000 * landsize
         return jsonify({'real_estate_price': price})
        else:
         return jsonify({'real_estate_price': 0, 'district': district, 'street': street})
@app.route('/house_price', methods=['POST'])
def get_house_price():
    data = request.get_json()
    floor_info = data['houseInfo']['value']['numberOfFloors']
    type_house = data['propertyBasicInfo']['typeOfRealEstate']['value']
    landsize = data["propertyBasicInfo"]["landSize"]['value']
    city = data['propertyBasicInfo']['address']['value']['city']

    if any(var is None for var in [landsize, type_house, floor_info, city]):
        return jsonify({'error': 'Input cannot be null.'})

    decoded_type_house = unidecode(type_house).lower()
    decoded_city = unidecode(city).lower()

    if decoded_city != " ha noi":
        return jsonify({'error': 'This feature will be updated soon.'})

    def price_type(type_house, floor_info):
        if type_house == 'fourLevelHouse' and floor_info > 1:
            return "Error: If fourLevelHouse and floor > 1, maybe your house is type oldStoreHouse"
        if type_house in ['newhouse', 'townhouse', 'oldstorehouse','privateproperty','shophouse']:
            if floor_info == 1:
                return  (2351000, 4569000)
            elif floor_info in [2, 3]:
                return  6163000
            elif floor_info in [4, 5]:
                return  (6122000, 7038000)
            elif floor_info in [6, 7, 8]:
                return  6249000
        elif type_house in ['apartment', 'miniapartment']:
            if floor_info > 5:
                return  (6704000, 7481000)
            else : return 'No apartment under 3 floor'
        elif type_house in ['resort']:
            return (7547000,7553000)
        else:return 0
    price = 0
    if  isinstance(landsize, str) or  isinstance(floor_info, str):
        return jsonify({'error': 'Landsize and floor_info must be number.'})
    house_price = price_type(decoded_type_house, floor_info)
    if isinstance(house_price, str):
        return jsonify({'error': house_price})
    elif isinstance(house_price, int):
        price = house_price * floor_info
    elif isinstance(house_price, tuple):
        price = tuple(x * floor_info for x in house_price)
    if isinstance(price, int):
        house_price = price * landsize
    elif isinstance(price, tuple):
        house_price = tuple(x * landsize for x in price)

    return jsonify({'house_price':house_price })

if __name__ == '__main__':
    app.run()





