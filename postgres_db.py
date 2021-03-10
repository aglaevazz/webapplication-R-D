# The MyPostgres class communicates with the postgres database.
# The database holds two tables: countries and gdp_expenditure_on_r_and_d.
# Find the schema and csv-files  in the folder 'database-init'
# The original data can be found on https://ec.europa.eu/eurostat/databrowser/view/t2020_20/default/table?lang=en

import psycopg2
from psycopg2 import sql


class MyPostgres:
    def __init__(self, db_name='europe', username='postgres', password='postgres'):
        self.db_name = db_name
        self.username = username
        self.password = password

    def get_top_10_countries_spending_most_gdp_for_r_and_d(self):
        with psycopg2.connect(dbname=self.db_name, user=self.username, password=self.password, host="localhost") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                SELECT countries.name, ROUND(gdp_expenditure_on_r_and_d._2019::numeric, 2)
                FROM gdp_expenditure_on_r_and_d
                RIGHT JOIN countries
                ON countries.code = gdp_expenditure_on_r_and_d.country_code
                WHERE gdp_expenditure_on_r_and_d._2019 IS NOT NULL AND LENGTH(countries.code) = 2
                ORDER BY 2 DESC, 1
                LIMIT 10;
                ''')
                result = cur.fetchall()
                return result

    def get_top_10_countries_spending_least_gdp_for_r_and_d(self):
        with psycopg2.connect(dbname=self.db_name, user=self.username, password=self.password, host="localhost") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                SELECT countries.name, ROUND(gdp_expenditure_on_r_and_d._2019::numeric, 2)
                FROM gdp_expenditure_on_r_and_d
                RIGHT JOIN countries
                ON countries.code = gdp_expenditure_on_r_and_d.country_code
                WHERE countries.code = gdp_expenditure_on_r_and_d.country_code AND gdp_expenditure_on_r_and_d._2019 IS NOT NULL AND LENGTH(countries.code) = 2
                ORDER BY 2, 1
                LIMIT 10;
                ''')
                result = cur.fetchall()
                cur.close()
                return result

    def get_gdp_expenditure_on_r_and_d_for_each_country(self):
        with psycopg2.connect(dbname=self.db_name, user=self.username, password=self.password, host="localhost") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                SELECT countries.name, ROUND(gdp_expenditure_on_r_and_d._2019::numeric, 2)
                FROM gdp_expenditure_on_r_and_d
                RIGHT JOIN countries
                ON countries.code = gdp_expenditure_on_r_and_d.country_code
                WHERE gdp_expenditure_on_r_and_d._2019 IS NOT NULL
                ORDER BY 1;
                ''')
                result = cur.fetchall()
                cur.close()
                return result

    def get_all_countries_names(self):
        with psycopg2.connect(dbname=self.db_name, user=self.username, password=self.password, host="localhost") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT DISTINCT(name)
                    FROM countries
                    ORDER BY name;''')
                result = cur.fetchall()
                cur.close()
                return result

    def get_matching_countries(self, partial_country_name):
        with psycopg2.connect(dbname=self.db_name, user=self.username, password=self.password, host="localhost") as conn:
            with conn.cursor() as cur:
                query = sql.SQL('''
                    SELECT name 
                    FROM countries 
                    WHERE code LIKE UPPER(%s) OR LOWER(name) LIKE LOWER(%s)
                    ''').format(pkey=sql.Identifier('country'))
                partial_country_name = partial_country_name + '%'
                cur.execute(query, (partial_country_name, partial_country_name))
                result = cur.fetchall()
                cur.close()
                return result

    def get_countries_gdp_expenditure_history(self, country):
        with psycopg2.connect(dbname=self.db_name, user=self.username, password=self.password, host="localhost") as conn:
            with conn.cursor() as cur:
                query = sql.SQL('''
                SELECT * FROM gdp_expenditure_on_r_and_d
                RIGHT JOIN countries
                ON countries.code = gdp_expenditure_on_r_and_d.country_code
                WHERE countries.code = %s OR LOWER(countries.name) LIKE LOWER(%s)
                ''').format(pkey2=sql.Identifier('country_code'), pkey3=sql.Identifier('country_wildcard'))
                country_wildcard = country + '%'
                cur.execute(query, (country, country_wildcard))
                result = cur.fetchall()
                cur.close()
                return result
