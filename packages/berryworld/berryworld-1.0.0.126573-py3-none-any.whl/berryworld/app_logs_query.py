import requests
import json
import pandas as pd


class AppLogsQuery:
    """ Query Logs to ApplicationInsights """

    def __init__(self, app_id, app_key, days=1):
        """ Initialize the class
        :param app_id: ApplicationId as it comes in Application Insights -> API Access
        :param app_key: ApplicationKey as it comes in Application Insights -> API Access
        :param days: Days to query back the logs (Applicable only if using the default Kusto query)
        """
        self.headers = {'X-Api-Key': app_key}
        self.url = f'https://api.applicationinsights.io/v1/apps/{app_id}/query'

        default_kusto_query = f"""
          exceptions
          | where timestamp > ago({days}d) 
          | order by timestamp
        """
        self.params = {"query": default_kusto_query}
        self.exception_params = {"query": default_kusto_query}

    def query_logs(self, query=None):
        """ Query Application Insights logs
        :param query: Kusto query to retrieve the logs
        """

        if query is not None:
            self.params = {"query": query}

        # Query logs
        app_ins_resp = requests.get(self.url, headers=self.headers, params=self.params)
        logs = json.loads(app_ins_resp.text)

        # Load logs into a DataFrame
        logs_df = pd.DataFrame()
        for row in logs['tables'][0]['rows']:
            logs_df = pd.concat([logs_df, pd.DataFrame(row).T])
        columns_list = pd.DataFrame(logs['tables'][0]['columns'])['name'].values
        logs_df.columns = columns_list

        return logs_df.drop_duplicates().reset_index(drop=True)

    def query_exceptions(self):
        """ Query Application Insights logs
        """
        # Query logs
        app_ins_resp = requests.get(self.url, headers=self.headers, params=self.exception_params)
        logs = json.loads(app_ins_resp.text)

        # Convert Logs into a DataFrame
        logs_df = pd.DataFrame()
        for row in logs['tables'][0]['rows']:
            logs_df = pd.concat([logs_df, pd.DataFrame(row).T])

        columns_list = pd.DataFrame(logs['tables'][0]['columns'])['name'].values
        logs_df.columns = columns_list

        logs_df = logs_df[
            ['timestamp', 'severityLevel', 'details', 'customDimensions', 'client_CountryOrRegion']].drop_duplicates()

        # Standardise timestamp
        logs_df['timestamp'] = pd.to_datetime(logs_df['timestamp'])
        logs_df['timestamp'] = logs_df['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Unpack Custom Dimensions and Error Messages
        logs_df = logs_df.assign(**pd.json_normalize(logs_df['customDimensions'].apply(lambda x: json.loads(x))))
        logs_df = logs_df.assign(**pd.json_normalize(logs_df['details'].apply(lambda x: json.loads(x)[0])))

        logs_df = logs_df.rename(columns={'timestamp': 'RaisedAt', 'severityLevel': 'SeverityLevel',
                                          'client_CountryOrRegion': 'Country', 'message': 'ErrorMessage'})

        if any(['projectname' == col.lower() for col in logs_df.columns]):
            logs_df = logs_df[['RaisedAt', 'SeverityLevel', 'Country', 'ProjectName',
                               'Pipeline', 'IpAddress', 'RequestUrl', 'ErrorMessage']]
        else:
            logs_df = logs_df[['RaisedAt', 'SeverityLevel', 'Country', 'ErrorMessage']]

        return logs_df
