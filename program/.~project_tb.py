import backend
from backend import insert_dog

class TestBackendFunctions():

    #since the program is basically talking to the database, all we care is the queries
    #thus, we mainly test whether the backend can output a correct query for the database input
    #test whether insert method works
    def test_insert_shelter(self):
        org_id = "123"
        shelter_city = "Example City"
        shelter_state = "Example State"
        zip_code = "12345"

        backend.query = insert_shelter(org_id, shelter_city, shelter_state, zip_code)
        expected = """INSERT INTO shelter (org_id, state, city, zip)
                    VALUES(123, Example City, Example State, 12345)"""
        
        self.assertEqual(result, expected, f"Expected '{expected}', but a wrong is returned '{result}'")

    #test insert new dog info
    def test_insert_dog(self):
        org_id = "?"
        id = "?"
        contact_city = "?"
        url = "?"
        breed_primary = "?"
        age = "?"
        sex = "?"
        size = "?"
        house_trained = "?"
        shots_current,name = "?"
        description = "?"

        test_insert_dog.query = insert_dog(id,org_id,contact_city,url, breed_primary,age,sex,size, house_trained,shots_current,name, description)
        expected = """INSERT INTO dog (id, org_id, contact_city, url, breed_primary, 
                    age, sex, size, house_trained, shots_current, name, description)
                    VALUES(?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        self.assertEqual(result, expected, f"Expected '{expected}', but a wrong is returned '{result}'")


    #test inserting new requirement to the database
    def test_insert_require(self):
        age = "young"
        requirement = "aa"
        vac_stat = "CA"

        result = insert_require(requirement,vac_stat, age)
        expected = """INSERT INTO requirement (state, requirement, age)
            VALUES(CA,aa,young);"""
        self.assertEqual(result, expected, f"Expected '{expected}', but a wrong is returned '{result}'")

     #test searching dogs
    def test_insert_require(self):
        zipcode = "0"
        city = "a"
        state = "AA"

        result = dogs_perform_search(zipcode, city, state)
        expected = """SELECT d.name, d.breed_primary, d.age, d.shots_current,d.size, d.description
                    FROM dog d, shelter s
                    WHERE d.org_id = s.org_id 
                    AND d.contact_city = s.city
                    AND s.zip = 0 ;"""
        self.assertEqual(result, expected, f"Expected '{expected}', but a wrong is returned '{result}'")

    

if __name__ == '__main__':
    unittest.main()
