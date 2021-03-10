from flask import Flask, render_template, request, redirect, url_for
from postgres_db import MyPostgres


app = Flask(__name__)
db = MyPostgres()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/queryCountryHistory", methods=["POST", "GET"])
def query_country_history_gdp_expenditure_on_r_and_d():
    error = request.args.get('error')
    available_countries = db.get_all_countries_names()
    if request.method == "POST":
        requested_country = request.form["country"]
        return redirect(url_for("handle_query_country_history_gdp_expenditure_on_r_and_d", country=requested_country))
    if error == 'not_a_country':
        return render_template("query_country_history.html", available_countries=available_countries,
                               additional_information="Sorry, this input didn't match a country.")
    elif error == 'input_too_short':
        return render_template("query_country_history.html", available_countries=available_countries,
                               additional_information="Sorry, this input is too short.")
    elif error == 'ambiguous_country':
        matching_countries = request.args.get('countries')
        return render_template("query_country_history.html", available_countries=available_countries,
                               additional_information="Your input matched the following countries, please be more specific.",
                               matching_countries=matching_countries)
    return render_template("query_country_history.html", available_countries=available_countries)


@app.route("/countryInfo")
def handle_query_country_history_gdp_expenditure_on_r_and_d():
    country = request.args.get('country')
    available_countries = db.get_all_countries_names()
    if len(country) >= 2:
        matching_countries = db.get_matching_countries(country)
        if not matching_countries:
            return redirect(url_for("query_country_history_gdp_expenditure_on_r_and_d",
                                    available_countries=available_countries, error='not_a_country'))
        elif len(matching_countries) > 1:
            matching_countries = ', '.join(entry[0] for entry in matching_countries)
            return redirect(url_for("query_country_history_gdp_expenditure_on_r_and_d",
                                    available_countries=available_countries,
                                    error='ambiguous_country', countries=matching_countries))
        else:
            country = matching_countries[0][0]
            gdp_expenditure_on_r_and_d_since_1990 = db.get_countries_gdp_expenditure_history(country)[0][1:-2]
            gdp_expenditure_on_r_and_d_since_1990 = \
                [(year, entry) for year, entry in enumerate(gdp_expenditure_on_r_and_d_since_1990, start=1990)]
            return render_template("country_report.html", country=country,
                                   gdp_expenditure_on_r_and_d_since_1990=gdp_expenditure_on_r_and_d_since_1990)
    return redirect(url_for("query_country_history_gdp_expenditure_on_r_and_d",
                            available_countries=available_countries, error='input_too_short'))


@app.route("/Report2019")
def report_2019():
    top_10_countries_most_gdp_for_r_and_d = db.get_top_10_countries_spending_most_gdp_for_r_and_d()
    top_10_countries_least_gdp_for_r_and_d = db.get_top_10_countries_spending_least_gdp_for_r_and_d()
    gdp_for_r_and_d_per_country = db.get_gdp_expenditure_on_r_and_d_for_each_country()
    return render_template("report_2019.html",
                           top_10_countries_most_gdp_for_RandD=top_10_countries_most_gdp_for_r_and_d,
                           top_10_countries_least_gdp_for_RandD=top_10_countries_least_gdp_for_r_and_d,
                           gpp_for_RandD_per_country=gdp_for_r_and_d_per_country)


if __name__ == '__main__':
    app.run()
