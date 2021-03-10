import unittest
from mock import Mock
from flask_app import app


class TestFlaskAppUnittest(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()

    # TEST HOME ENDPOINT

    def test_home(self):
        response = self.tester.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"This web-application provides information"
        self.assertTrue(html_as_bytes in response.data)

    # TEST QUERY_AIRPORTS ENDPOINT

    # access page
    def test_query_country_history_gdp_expenditure_on_r_and_d_1(self):
        response = self.tester.get("/queryCountryHistory")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = \
            b"Enter the name of the country or the country-code"
        self.assertTrue(html_as_bytes in response.data)

    # call post method with user_input
    def test_query_country_history_gdp_expenditure_on_r_and_d_2(self):
        response = self.tester.post("/queryCountryHistory", data={"country": ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"Redirecting"
        self.assertTrue(html_as_bytes in response.data)

    # error = entered string is not a country
    def test_query_country_history_gdp_expenditure_on_r_and_d_3(self):
        request = Mock()
        request.args.get('error').return_value = 'not_a_country'
        response = self.tester.get("/queryCountryHistory?error=not_a_country#")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"Sorry, this input"
        self.assertTrue(html_as_bytes in response.data)

    # error = entered string is smaller than two letter
    def test_query_country_history_gdp_expenditure_on_r_and_d_4(self):
        request = Mock()
        request.args.get('error').return_value = 'input_too_short'
        response = self.tester.get("/queryCountryHistory?error=input_too_short#")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"Sorry, this input is too short."
        self.assertTrue(html_as_bytes in response.data)

    # error = entered string matches various countries
    def test_query_country_history_gdp_expenditure_on_r_and_d_5(self):
        request = Mock()
        request.args.get('error').return_value = 'ambiguous_country'
        response = self.tester.get("/queryCountryHistory?error=ambiguous_country#")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"Your input matched the following countries"
        self.assertTrue(html_as_bytes in response.data)

    # TEST HANDLE_QUERY_AIRPORTS ENDPOINT

    # input string (country) is smaller then two characters
    def test_handle_query_country_history_gdp_expenditure_on_r_and_d_1(self):
        response = self.tester.get("/countryInfo?country=a#")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"Redirecting"
        self.assertTrue(html_as_bytes in response.data)

    # no matching countries
    def test_handle_query_country_history_gdp_expenditure_on_r_and_d_2(self):
        response = self.tester.get("/countryInfo?country=aaaa1ffg#")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"not_a_country"
        self.assertTrue(html_as_bytes in response.data)

    # various matching countries
    def test_handle_query_country_history_gdp_expenditure_on_r_and_d_3(self):
        response = self.tester.get("/countryInfo?country=de#")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"ambiguous_country"
        self.assertTrue(html_as_bytes in response.data)

    # one matching country
    def test_handle_query_country_history_gdp_expenditure_on_r_and_d_4(self):
        response = self.tester.get("/countryInfo?country=germany#")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"Information on: Germany"
        self.assertTrue(html_as_bytes in response.data)
        html_as_bytes = b"1993: 2.21%"
        self.assertTrue(html_as_bytes in response.data)

    # TEST REPORT ENDPOINT

    def test_report_2019(self):
        response = self.tester.get("/Report2019")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        html_as_bytes = b"Top 10 Countries with Highest Percentage of GDP Used for R&D"
        self.assertTrue(html_as_bytes in response.data)


if __name__ == "__main__":
    unittest.main()
