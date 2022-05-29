import csv
import psycopg2

def fill_tables():
    """
    Fill the table Movie with all the movies in movies.csv
    """
    # connect to the databse
    conn = psycopg2.connect("host=db dbname=db_movies user=secureUser1 password=TotalySecurePass1")
    cursor = conn.cursor()
    # check if the table is empty
    sql = """SELECT count(*) as tot FROM search_movie"""
    cursor.execute(sql)
    data = cursor.fetchone()
    #only fill the db if the table is empty
    if data[0]<1:
        cur = conn.cursor()
        # base query to add a movie
        sql= "INSERT INTO search_movie (title, description, year, runtime) VALUES (%s, %s, %s, %s)"
        # open movies.csv
        file_object = open("/app/movies.csv", "r")
        csvf = csv.reader(file_object, delimiter = ",")
        first = True
        # go over all the lines
        for row in csvf:
            # skip the header
            if first:
                first=False
                continue
            # add the movie
            cur.execute(sql, (row[0], row[1], row[2], row[3]))
        # send to the db
        conn.commit()