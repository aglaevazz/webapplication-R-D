import unittest
from mock import Mock
from flask_app import app


class TestFlaskAppUnittest(unittest.TestCase):

    # TEST HOME ENDPOINT

    def test_home_status_code(self):
        tester = app.test_client()
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_mime(self):
        tester = app.test_client()
        response = tester.get("/")
        self.assertEqual(response.mimetype, "text/html")

    def test_home_data(self):
        tester = app.test_client()
        response = tester.get("/")
        html_as_bytes = b"This web-application provides information about airports around the world."
        self.assertTrue(html_as_bytes in response.data)

    # TEST QUERY_AIRPORTS ENDPOINT

    # access page
    def test_query_airports_status_code_1(self):
        tester = app.test_client()
        response = tester.get("/queryAirports")
        self.assertEqual(response.status_code, 200)

    # access page
    def test_query_airports_mime_1(self):
        tester = app.test_client()
        response = tester.get("/queryAirports")
        self.assertEqual(response.mimetype, "text/html")

    # access page
    def test_query_airports_data_1(self):
        tester = app.test_client()
        response = tester.get("/queryAirports")
        html_as_bytes = \
            b"Enter the name of the country or the country-code to see available airports and respective runway-types."
        self.assertTrue(html_as_bytes in response.data)

    # call post method with user_input
    def test_query_airports_status_code_2(self):
        tester = app.test_client()
        response = tester.post("/queryAirports", data={"country": ''})
        self.assertEqual(response.status_code, 302)

    # call post method with user_input
    def test_query_airports_mime_2(self):
        tester = app.test_client()
        response = tester.post("/queryAirports", data={"country": ''})
        self.assertEqual(response.mimetype, "text/html")

    # call post method with user_input
    def test_query_airports_data_2(self):
        tester = app.test_client()
        response = tester.post("/queryAirports", data={"country": ''})
        html_as_bytes = b"Redirecting"
        self.assertTrue(html_as_bytes in response.data)

    # error = entered string is not a country
    def test_query_airports_status_code_3(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'not_a_country'
        response = tester.get("/queryAirports?error=not_a_country#")
        self.assertEqual(response.status_code, 200)

    # error = entered string is not a country
    def test_query_airports_mime_3(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'not_a_country'
        response = tester.get("/queryAirports?error=not_a_country#")
        self.assertEqual(response.mimetype, "text/html")

    # error = entered string is not a country
    def test_query_airports_data_3(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'not_a_country'
        response = tester.get("/queryAirports?error=not_a_country#")
        html_as_bytes = b"Sorry, this input"
        self.assertTrue(html_as_bytes in response.data)

    # error = entered string is smaller than two letter
    def test_query_airports_status_code_4(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'input_too_short'
        response = tester.get("/queryAirports?error=input_too_short#")
        self.assertEqual(response.status_code, 200)

    # error = entered string is smaller than two letter
    def test_query_airports_mime_4(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'input_too_short'
        response = tester.get("/queryAirports?error=input_too_short#")
        self.assertEqual(response.mimetype, "text/html")

    # error = entered string is smaller than two letter
    def test_query_airports_data_4(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'input_too_short'
        response = tester.get("/queryAirports?error=input_too_short#")
        html_as_bytes = b"Sorry, this input is too short."
        self.assertTrue(html_as_bytes in response.data)

    # error = entered string matches various countries
    def test_query_airports_status_code_5(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'ambiguous_country'
        response = tester.get("/queryAirports?error=ambiguous_country#")
        self.assertEqual(response.status_code, 200)

    # error = entered string matches various countries
    def test_query_airports_mime_5(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'ambiguous_country'
        response = tester.get("/queryAirports?error=ambiguous_country#")
        self.assertEqual(response.mimetype, "text/html")

    # error = entered string matches various countries
    def test_query_airports_data_5(self):
        tester = app.test_client()
        request = Mock()
        request.args.get('error').return_value = 'ambiguous_country'
        response = tester.get("/queryAirports?error=ambiguous_country#")
        html_as_bytes = b"Your input matched the following countries"
        self.assertTrue(html_as_bytes in response.data)

    # TEST HANDLE_QUERY_AIRPORTS ENDPOINT

    # input string (country) is smaller then two characters
    def test_handle_query_airports_status_code_1(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=a#")
        self.assertEqual(response.status_code, 302)

    # input string (country) is smaller then two characters
    def test_handle_query_airports_mime_1(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=a#")
        self.assertEqual(response.mimetype, "text/html")

    # input string (country) is smaller then two characters
    def test_handle_query_airports_data_1(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=a#")
        html_as_bytes = b"Redirecting"
        self.assertTrue(html_as_bytes in response.data)

    # no matching countries
    def test_handle_query_airports_status_code_2(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=aaaa1ffg#")
        self.assertEqual(response.status_code, 302)

    # no matching countries
    def test_handle_query_airports_mime_2(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=aaaa1ffg#")
        self.assertEqual(response.mimetype, "text/html")

    # no matching countries
    def test_handle_query_airports_data_2(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=aaaa1ffg#")
        html_as_bytes = b"not_a_country"
        self.assertTrue(html_as_bytes in response.data)

    # various matching countries
    def test_handle_query_airports_status_code_3(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=an#")
        self.assertEqual(response.status_code, 302)

    # various matching countries
    def test_handle_query_airports_mime_3(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=an#")
        self.assertEqual(response.mimetype, "text/html")

    # various matching countries
    def test_handle_query_airports_data_3(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=an#")
        html_as_bytes = b"ambiguous_country"
        self.assertTrue(html_as_bytes in response.data)

    # one matching countries
    def test_handle_query_airports_status_code_4(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=andorra#")
        self.assertEqual(response.status_code, 200)

    # one matching countries
    def test_handle_query_airports_mime_4(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=andorra#")
        self.assertEqual(response.mimetype, "text/html")

    # one matching countries
    def test_handle_query_airports_data_4(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=andorra#")
        html_as_bytes = b"Information on: Andorra"
        self.assertTrue(html_as_bytes in response.data)

    # one matching countries
    def test_handle_query_airports_data_5(self):
        tester = app.test_client()
        response = tester.get("/countryInfo?country=andorra#")
        html_as_bytes = b"Andorra la Vella Heliport: N/A"
        self.assertTrue(html_as_bytes in response.data)

    # TEST REPORT ENDPOINT

    def test_report_status_code(self):
        tester = app.test_client()
        response = tester.get("/Report")
        self.assertEqual(response.status_code, 200)

    def test_report_mime(self):
        tester = app.test_client()
        response = tester.get("/Report")
        self.assertEqual(response.mimetype, "text/html")

    def test_report_data(self):
        tester = app.test_client()
        response = tester.get("/Report")
        html_as_bytes = b"Top 10 Countries with the Highest Number of Airports"
        self.assertTrue(html_as_bytes in response.data)


if __name__ == "__main__":
    unittest.main()
