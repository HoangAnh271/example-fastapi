from typing import Union
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class RealEstate(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float = 0


    #area: float = 0
while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='myfamily270103', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

# version with no postgres in pgAdmin 4
# my_re = [{"name": "name of real estate 1", "description": "description of real estate 1", "id": 1},
#          {"name": "Ho Chi Minh's real estate", "description": "good price and good place", "id": 2}]

# def find_real_estate(id):
#     for re in my_re:
#         if re['id'] == id:
#             return re


# def find_index_real_estate(id):
#     for i, re in enumerate(my_re):
#         if re['id'] == id:
#             return i


@app.get("/")
def root():
    return {"message": "welcome to real estate API"}


@app.get("/realestates")
def get_real_estates():
    cursor.execute("""SELECT * FROM real_estates """)
    real_estates = cursor.fetchall()
    return {"data": real_estates}


@app.post("/realestates", status_code=status.HTTP_201_CREATED)
def create_real_estates(real_estate: RealEstate):
    # real_estate_dict = real_estate.dict() #version with no postgres  in pdAdmin 4
    # real_estate_dict['id'] = randrange(0, 100000)
    # my_re.append(real_estate_dict)
    cursor.execute("""INSERT INTO real_estates (name, description, price) VALUES (%s, %s, %s) RETURNING * """,
                   (real_estate.name, real_estate.description, real_estate.price))
    new_real_estate = cursor.fetchone()

    conn.commit()

    return {"data": new_real_estate}


@app.get("/realestates/{id}")
def get_real_estate(id: int):
    cursor.execute("""SELECT * FROM real_estates WHERE id = %s """, (str(id)))
    real_estate = cursor.fetchone()
    # real_estate = find_real_estate(id) # version with no postgres in pgAdmin 4
    if not real_estate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"real estate with id: {id} was not found")
    return {"real_estate_detail": real_estate}


@app.delete("/realestates/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_real_estate(id: int):
    # index = find_index_real_estate(id) # version with no postgres in pgAdmin 4
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"real estate with id: {id} does not exist")
    # my_re.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    cursor.execute(
        """DELETE FROM real_estates WHERE id = %s RETURNING *""", (str(id)))
    deleted_real_estate = cursor.fetchone()

    conn.commit()

    if deleted_real_estate == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"real estate with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/realestates/{id}")
def update_real_estate(id: int, real_estate: RealEstate):
    # index = find_index_real_estate(id) # version with no postgres

    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"real estate with id: {id} does not exist")

    # real_estate_dict = real_estate.dict()
    # real_estate_dict['id'] = id
    # my_re[index] = real_estate_dict
    # return {"data": real_estate_dict}
    cursor.execute("""UPDATE real_estates SET name = %s, description = %s, price = %s WHERE id = %s RETURNING *""",
                   (real_estate.name, real_estate.description, real_estate.price, str(id)))
    updated_real_estate = cursor.fetchone()

    conn.commit()

    if updated_real_estate == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")

    return {"data": updated_real_estate}
