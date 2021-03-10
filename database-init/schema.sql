CREATE TABLE IF NOT EXISTS countries (
  code            VARCHAR(10) NOT NULL PRIMARY KEY,
  name            VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS gdp_expenditure_on_r_and_d(
  country_code    VARCHAR(10) NOT NULL PRIMARY KEY,
  _1990           REAL,
  _1991           REAL,
  _1992           REAL,
  _1993           REAL,
  _1994           REAL,
  _1995           REAL,
  _1996           REAL,
  _1997           REAL,
  _1998           REAL,
  _1999           REAL,
  _2000           REAL,
  _2001           REAL,
  _2002           REAL,
  _2003           REAL,
  _2004           REAL,
  _2005           REAL,
  _2006           REAL,
  _2007           REAL,
  _2008           REAL,
  _2009           REAL,
  _2010           REAL,
  _2011           REAL,
  _2012           REAL,
  _2013           REAL,
  _2014           REAL,
  _2015           REAL,
  _2016           REAL,
  _2017           REAL,
  _2018           REAL,
  _2019           REAL
);
