import pandas as pd
import sqlite3 as sql
import re

formatted_query = ""

def insert_dog(id,org_id,contact_city,url, breed_primary,age,sex,size, house_trained,shots_current,name, description):
    # Initialize empty lists to store the results
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    global formatted_query
    query = """INSERT INTO dog (id, org_id, contact_city, url, breed_primary, 
                    age, sex, size, house_trained, shots_current, name, description)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}', '{6}','{7}','{8}','{9}','{10}','{11}');"""
    formatted_query = query.format(id,org_id,contact_city,url, breed_primary,age,sex,size, house_trained,shots_current,name, description)
    cursor.execute(formatted_query)

        
    # Close the connection to the database
    conn.close()

def insert_require(requirement,vac_stat, age):
    # Initialize empty lists to store the results
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    global formatted_query
    query = """INSERT INTO requirement (state, requirement, age)
            VALUES('{0}','{1}','{2}');"""
    formatted_query = query.format(state, requirement, age)
    cursor.execute(formatted_query)

    
    # Close the connection to the database
    conn.close()

def insert_shelter(org_id,shelter_city,shelter_state, zip_code):
    # Initialize empty lists to store the results
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    global formatted_query
    query = """INSERT INTO shelter (org_id, state, city, zip)
                    VALUES('{0}','{1}','{2}','{3}');"""
    formatted_query = query.format(org_id,shelter_city,shelter_state, zip_code)
    cursor.execute(formatted_query)
    # Close the connection to the database
    conn.close()

def dogs_perform_search(zipcode, city, state):
    global formatted_query
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    #dog_info = f"{dog_name} - Breed: {dog_breed}, Age: {dog_age}, shots_current: {dog_shots_current}, size: {dog_size}, description: {dog_description}"
      # dog query - Search by zipcode first 
    
    dogs_query = """SELECT d.name, d.breed_primary, d.age, d.shots_current,d.size, d.description
                    FROM dog d, shelter s
                    WHERE d.org_id = s.org_id 
                    AND d.contact_city = s.city
                    AND s.zip = '{0}' ;"""
    formatted_query = dogs_query.format(zipcode)
    cursor.execute(formatted_query)
    dogs_results = cursor.fetchall()
    
    # If no results found from the first query, perform the second MySQL query based on city and state and sort by value2
    if not dogs_results:
        dogs_query = """SELECT d.name, d.breed_primary, d.age, d.shots_current,d.size, d.description
                        FROM dog d, shelter s
                        WHERE d.org_id = s.org_id 
                        AND d.contact_city = s.city
                        AND s.city = '{0}' 
                        AND s.state = '{1}';"""
        formatted_query = dogs_query.format(city, state)
        cursor.execute(formatted_query)
        dogs_results = cursor.fetchall()
    if not dogs_results:
        dogs_query = """SELECT d.name, d.breed_primary, d.age, d.shots_current,d.size, d.description 
                        FROM dog d, shelter s
                        WHERE s.state = '{0}' 
                        AND d.org_id = s.org_id
                        AND d.contact_city = s. city;"""
        
     
        formatted_query = dogs_query.format(state)
        cursor.execute(formatted_query)
        dogs_results = cursor.fetchall()
    # Close the connection to the database
    conn.close()
    return dogs_results

def pet_store_perform_search(zipcode, city, state):
    global formatted_query
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    # petstore query - Search by zipcode first 
    pet_care_query = """SELECT * 
                          FROM pet_care c 
                          WHERE postal_code = '{0}' 
                          LIMIT 20;"""
    pet_stores_results = cursor.fetchall()
    formatted_query = pet_care_query.format(zipcode)
    cursor.execute(formatted_query)
    # If no results found from the first query, perform the second MySQL query based on city and state and sort by value2
    if not pet_stores_results:
        pet_care_query = """SELECT * 
                          FROM pet_care c 
                          WHERE city = '{0}'  
                          AND state = '{1}' 
                          LIMIT 20;"""
        formatted_query = pet_care_query.format(city, state)
        cursor.execute(formatted_query)
        pet_stores_results = cursor.fetchall()

    if not pet_stores_results:
        c = """SELECT * 
                          FROM pet_care c 
                          WHERE state = '{0}'
                          LIMIT 20;"""
        formatted_query = pet_stores_results.format(state)
        cursor.execute(formatted_query)
        pet_stores_results = cursor.fetchall()
        

    # Close the connection to the database
    conn.close()
    return pet_stores_results

def clinics_perform_search(zipcode, city, state):
    global formatted_query
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    # petstore query - Search by zipcode first 
    clinics_query = """SELECT * 
                       FROM clinics c 
                       WHERE postal_code = '{0}'
                       LIMIT 20;"""
    formatted_query = clinics_query.format(zipcode)
    cursor.execute(formatted_query)
    clinics_results = cursor.fetchall()
    
    # If no results found from the first query, perform the second MySQL query based on city and state and sort by value2
    if not clinics_results:
        clinics_query = """SELECT * 
                          FROM pet_care c 
                          WHERE city = '{0}' 
                          AND state = '{1}'
                          LIMIT 20;"""
        formatted_query = clinics_query.format(city, state)
        cursor.execute(formatted_query)
        clinics_results = cursor.fetchall()

    if not clinics_results:
        clnics_query = """SELECT * 
                          FROM pet_care c 
                          WHERE state = '{0}'
                          LIMIT 20;"""
        formatted_query = clinics_query.format(state)
        cursor.execute(formatted_query)
        clinics_results = cursor.fetchall()
    

    # Close the connection to the database
    conn.close()
    return clinics_results

def government_perform_search(zipcode, city, state):
    # Initialize empty lists to store the results
    global formatted_query
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
  
    government_query = """SELECT * 
                            FROM shelter s, requirement r
                            WHERE r.state = '{0}'
                            AND r.state = s.state 
                            LIMIT 1;"""
    formatted_query = government_query.format(state)
    cursor.execute(formatted_query)
    government_results = cursor.fetchall()

    conn.close()
    
    return government_results

def sort_dog(zipcode, city, state, sex, breed, size, age):
    global formatted_query
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    # Create a list to store the conditions
    conditions = []
    parameters = []

    if sex:
        conditions.append("d.sex = ?")
        parameters.append(sex)
    if breed:
        conditions.append("d.breed_primary = ?")
        parameters.append(breed)
    if size:
        conditions.append("d.size = ?")
        parameters.append(size)
    if age:
        conditions.append("d.age = ?")
        parameters.append(age)
    query = ''
    # Combine the conditions with 'AND' operator
    if conditions:
        query += " AND " + " AND ".join(conditions)

    dogs_query = """SELECT d.name, d.breed_primary, d.age, d.shots_current, d.size, d.description
                    FROM dog d, shelter s
                    WHERE d.org_id = s.org_id 
                    AND d.contact_city = s.city
                    AND s.zip = ?""" + query + ";"
    
    cursor.execute(dogs_query, tuple([zipcode] + parameters))
    
    formatted_query = dogs_query.replace('?', '{}').format(*tuple([zipcode] + parameters))
    dogs_results = cursor.fetchall()


    # If no results found from the first query, perform the second MySQL query based on city and state and sort by value2
    if not dogs_results:
        dogs_query = """SELECT d.name, d.breed_primary, d.age, d.shots_current,d.size, d.description
                        FROM dog d, shelter s
                        WHERE d.org_id = s.org_id 
                        AND d.contact_city = s.city
                        AND s.city = ? 
                        AND s.state = ?""" + query + ";"
        cursor.execute(dogs_query, tuple([city, state] +  parameters))
        formatted_query = dogs_query.replace('?', '{}').format(*tuple([city,state] + parameters))
        dogs_results = cursor.fetchall()

    if not dogs_results:
        dogs_query = """SELECT d.name, d.breed_primary, d.age, d.shots_current,d.size, d.description 
                        FROM dog d, shelter s
                        WHERE s.state = ?
                        AND d.org_id = s.org_id
                        AND d.contact_city = s. city""" + query + ";"
        
        cursor.execute(dogs_query, tuple([state] + parameters))
        formatted_query = dogs_query.replace('?', '{}').format(*tuple([state] + parameters))
        dogs_results = cursor.fetchall()
    # Close the connection to the database
    conn.close()
    return dogs_results

def sort_pet_store(zipcode, city, state):
    global formatted_query
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    # petstore query - Search by zipcode first 
    pet_care_query = """SELECT stars, name, categories 
                          FROM pet_care c 
                          WHERE postal_code = '{0}'
                          ORDER BY c.stars DESC
                          LIMIT 20;"""
    formatted_query = pet_care_query.format(zipcode)
    cursor.execute(formatted_query)
    pet_stores_results = cursor.fetchall()

    # If no results found from the first query, perform the second MySQL query based on city and state and sort by value2
    if not pet_stores_results:
        pet_care_query = """SELECT stars, name, categories  
                          FROM pet_care c 
                          WHERE city = '{0}' 
                          AND state = '{1}'
                          ORDER BY c.stars DESC
                          LIMIT 20;"""
        formatted_query = pet_care_query.format(city, state)
        cursor.execute(formatted_query)
        pet_stores_results = cursor.fetchall()


    if not pet_stores_results:
        pet_care_query = """SELECT stars, name, categories  
                          FROM pet_care c 
                          WHERE state = '{0}'
                          ORDER BY c.stars DESC
                          LIMIT 20;"""
        formatted_query = pet_care_query.format(state)
        cursor.execute(formatted_query)
        pet_stores_results = cursor.fetchall()
    

    # Close the connection to the database
    conn.close()
    return pet_stores_results

def sort_clinics(zipcode, city, state):
    database = "test1.db"
    conn = sql.connect(database)
    cursor = conn.cursor()
    # petstore query - Search by zipcode first 
    clinics_query = """SELECT stars, name, categories  
                          FROM clinics c 
                          WHERE postal_code = ? 
                          ORDER BY c.stars DESC
                          LIMIT 20;"""
    cursor.execute(clinics_query, (zipcode,))
    clinics_results = cursor.fetchall()

    # If no results found from the first query, perform the second MySQL query based on city and state and sort by value2
    if not clinics_results:
        clinics_query_query = """SELECT stars, name, categories  
                          FROM pet_care c 
                          WHERE city = ? 
                          AND state = ?
                          ORDER BY c.stars DESC
                          LIMIT 20;"""
        cursor.execute(clinics_query_query, (city, state))
        clinics_results = cursor.fetchall()


    if not clinics_results:
        clnics_query = """SELECT stars, name, categories  
                          FROM pet_care c 
                          WHERE state = ?
                          ORDER BY c.stars DESC
                          LIMIT 20;"""
        cursor.execute(clnics_query, (state,))
        clinics_results = cursor.fetchall()
    

    # Close the connection to the database
    conn.close()
    return clinics_results