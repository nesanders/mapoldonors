These scripts automate public records data collection and aggregation about political contributions from the Massachusetts Office of Campaign and Political Finance.

The [mapoldonors_getdata.py] script scrapes all individual contributor donor data from the site.  Data downloaded as of December 2019 (going back to Jan 2000, with substantial data starting Jan 2001) is recorded in [OCPF_IndividualContributor.zip].

The [mapoldonors_summarize.py] generates aggregated summaries of the downloaded data, providing configuration hooks to filter and group the donor data in different ways.  The configuration is controlled by a configuration file, such as the provided [default.ini].
