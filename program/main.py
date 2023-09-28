import pandas as pd
import random
from flask import Flask, request, jsonify
from flask import Flask, render_template, request, redirect
import backend

app = Flask(__name__,template_folder='./frontEnd')

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read() 
        return html

@app.route('/insert', methods=['GET'])
def show_insert_form():
    return render_template('insert.html')

@app.route('/submit_dog', methods=['POST'])
def submit_dog():
    # Get the data from the form
    id = request.form['id']
    org_id = request.form['org_id']
    contact_city = request.form['contact_city']
    url = request.form['url']
    breed_primary = request.form['breed_primary']
    age = request.form['age']
    sex = request.form['sex']
    size = request.form['size']
    house_trained = request.form['house_trained']
    shots_current = request.form['shots_current']
    name = request.form['name']
    description = request.form['description']

    # TODO: Append the data row to the dataset
    backend.insert_dog(id,org_id,contact_city,url, breed_primary,age,sex,size, house_trained,shots_current,name, description)

    # Redirect back to the form page after submission
    with open("index.html") as f:
        html = f.read() 
        return html
    
@app.route('/submit_shelter', methods=['POST'])
def submit_shelter():
    # Get the data from the form
    org_id = request.form['org_id']
    shelter_city = request.form['city']
    shelter_state = request.form['state']
    zip_code = request.form['zip']
    backend.insert_shelter(org_id,shelter_city,shelter_state, zip_code)
 
    # Redirect back to the form page after submission
    with open("index.html") as f:
        html = f.read() 
        return html

@app.route('/submit_requirements', methods=['POST'])
def submit_requirements():
    # Get the data from the form
    requirement = request.form['requirement']
    vac_state = request.form['state']
    age = request.form['age']

    # TODO: Append the data row to the dataset
    backend.insert_require(requirement,vac_stat, age)

    # Redirect back to the form page after submission
    with open("index.html") as f:
        html = f.read() 
        return html

@app.route('/search', methods=['POST'])
def search():
    global zipcode
    zipcode = request.form.get('zipcode')
    global city 
    city = request.form.get('city')
    global state
    state = request.form.get('state')
    
    # Call the backend functions to perform the search
    dogs_results = backend.dogs_perform_search(zipcode, city, state)
    formatted_results = []

    for row in dogs_results:
        dog_name = row[0]
        dog_breed = row[1]
        dog_age = row[2]
        dog_shots_current = row[3]
        dog_size = row[4]
        dog_description = row[5]

        dog_info = f"{dog_name} - Breed: {dog_breed}, Age: {dog_age}, shots_current: {dog_shots_current}, size: {dog_size}, description: {dog_description}"
        formatted_results.append(dog_info)
    # Pass the search results to the HTML template for rendering
    return render_template('dogs.html', dogs_results=formatted_results, zipcode =zipcode, city = city, state = state)

@app.route('/shot_true')
def shot_true():
    # Get the dog information from the query parameters
    dog_name = request.args.get('name')
    dog_breed = request.args.get('breed')
    dog_age = request.args.get('age')
    dog_size = request.args.get('size')
    dog_description = request.args.get('description')
    # TODO:get pet_stores_results
    formatted_pet = []
    pet_stores_results = backend.pet_store_perform_search(zipcode, city, state)
    for data in pet_stores_results:
        rating = data[6]
        org_name = data[1]
        categories = data[2]
        zip_code = data[5]
        current_city = data[3]
        current_state = data[4]
        formatted_pet.append((org_name, categories, current_city, current_state, zip_code, rating,))
        
    # Render the template with the dog information
    return render_template('Shot_True.html', name=dog_name, breed=dog_breed, age=dog_age, size=dog_size, description=dog_description, zipcode =zipcode, city = city, state = state, pet_stores_results = formatted_pet)

@app.route('/shot_false')
def shot_false():
    # Get the dog information from the query parameters
    dog_name = request.args.get('name')
    dog_breed = request.args.get('breed')
    dog_age = request.args.get('age')
    dog_size = request.args.get('size')
    dog_description = request.args.get('description')
    # TODO: GET governments_results, clinics_results, pet_stores_results
    formatted_pet = []
    pet_stores_results = backend.pet_store_perform_search(zipcode, city, state)
    for data in pet_stores_results:
        rating = data[6]
        org_name = data[1]
        categories = data[2]
        zip_code = data[5]
        current_city = data[3]
        current_state = data[4]
        formatted_pet.append((org_name, categories,current_city, current_state, zip_code, rating,))
        
    clinics_results = backend.clinics_perform_search(zipcode, city, state)
    formatted_clinics = []
    for data in clinics_results:
        rating = data[6]
        org_name = data[1]
        categories = data[2]
        zip_code = data[5]
        current_city = data[3]
        current_state = data[4]
        formatted_clinics.append(( org_name, categories, current_city, current_state,zip_code, rating,) )

    governments_results = backend.government_perform_search(zipcode, city, state)
    formatted_govern = []
    for data in governments_results:
        requirement_description = data[5]
        adopter_age = data[6]
        formatted_govern.append((state,requirement_description,adopter_age, ))

    return render_template('Shot_False.html', name=dog_name, breed=dog_breed, age=dog_age, size=dog_size, description=dog_description, zipcode =zipcode, city = city, state = state, governments_results =formatted_govern, clinics_results = formatted_clinics, pet_stores_results = formatted_pet)


@app.route('/next_page', methods=['GET'])
def next_page():
    dog_info = request.args.get('dogInfo')
    # Split the dog_info string using comma as the delimiter
    info_list = dog_info.split(', ')

    # Extract individual pieces of information
    dog_name = info_list[0].split(' - ')[0]
    dog_breed = info_list[0].split(' - ')[1]
    dog_age = info_list[1].split(': ')[1]
    dog_shots_current = info_list[2].split(': ')[1]
    dog_size = info_list[3].split(': ')[1]
    dog_description = info_list[4].split(': ')[1]

    if dog_shots_current == 'True':
        return redirect('/shot_true?name=' + dog_name + '&breed=' + dog_breed + '&age=' + dog_age + '&size=' + dog_size + '&description=' + dog_description + '&zipcode=' + zipcode + '&city=' + city  + '&state=' + state)
    else:
        return redirect('/shot_false?name=' + dog_name + '&breed=' + dog_breed + '&age=' + dog_age + '&size=' + dog_size + '&description=' + dog_description + '&zipcode=' + zipcode + '&city=' + city  + '&state=' + state)

@app.route('/api/sort', methods=['POST'])
def api_sort():
    sex = request.form.get('sex')
    breed = request.form.get('breed')
    size = request.form.get('size')
    age = request.form.get('age')

    sorted_results = backend.sort_dog(zipcode, city, state, sex, breed, size, age)
    sorted_dogs = [
        {
            "Name": result[0],
            "Breed": result[1],
            "Age": result[2],
            "Shots_current": result[3],
            "Size": result[4], 
            "Description": result[5]
        }
        for result in sorted_results
    ]
    return jsonify(sorted_dogs)

@app.route('/api/sort_pet_stores', methods=['GET'])
def sort_petStore():
    pet_stores_results = backend.sort_pet_store(zipcode, city, state)
    sorted_pet_stores = [
        {
            "Rating": result[0],
            "Name": result[1],
            "Catalog": result[2]
        }
        for result in pet_stores_results
    ]
    return jsonify(sorted_pet_stores)

@app.route('/api/sort_clinics', methods=['GET'])
def sort_clinic():
    clinics_results = backend.sort_clinics(zipcode, city, state)
    sorted_clinics = [
        {
            "Rating": result[0],
            "Name": result[1],
            "Catalog": result[2]
        }
        for result in clinics_results
    ]
    return jsonify(sorted_clinics)



if __name__ == '__main__':
    app.run(port=8080,host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.