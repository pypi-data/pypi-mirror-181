import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler


class AppLogs:
    """ Upload Logs to ApplicationInsights """

    def __init__(self, instrumentation_key, project_name=None, pipeline=None, ip_address=None, request_url=None):
        """ Initialize the class
        :param instrumentation_key: Key to access Application Insights from Azure portal
        :param project_name: Name of the project being run. it must be already declared in PythonEmailProjectSeverity
        :param pipeline: Pipeline name being run. It must identify the process being executed uniquely
        :param ip_address: IP Address
        :param request_url: URL requested by the client
        """
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(AzureLogHandler(
            connection_string=f"InstrumentationKey={instrumentation_key};"
                              f"IngestionEndpoint=https://westeurope-5.in.applicationinsights.azure.com/;"
                              f"LiveEndpoint=https://westeurope.livediagnostics.monitor.azure.com/")
        )

        if (project_name is not None) | (pipeline is not None) | (ip_address is not None) | (request_url is not None):
            self.properties = {'custom_dimensions': {
                'ProjectName': project_name if project_name is not None else '',
                'Pipeline': pipeline if pipeline is not None else '',
                'IpAddress': ip_address if ip_address is not None else '',
                'RequestUrl': request_url if request_url is not None else ''}
            }
        else:
            self.properties = None

    def send_log(self, error_message, error_type='exception'):
        """ Send a Log message
        :param error_message: Error message
        :param error_type: Type of error to raise.
            - exception
            - critical
            - info
            - warning
            - error
        """
        if self.properties is None:
            if error_type == 'exception':
                self.logger.exception(error_message)
            elif error_type == 'critical':
                self.logger.critical(error_message)
            elif error_type == 'info':
                self.logger.info(error_message)
            elif error_type == 'warning':
                self.logger.warning(error_message)
            elif error_type == 'error':
                self.logger.error(error_message)
            else:
                raise Exception("error_type not understood")
        else:
            if error_type == 'exception':
                self.logger.exception(error_message, extra=self.properties)
            elif error_type == 'critical':
                self.logger.critical(error_message, extra=self.properties)
            elif error_type == 'info':
                self.logger.info(error_message, extra=self.properties)
            elif error_type == 'warning':
                self.logger.warning(error_message, extra=self.properties)
            elif error_type == 'error':
                self.logger.error(error_message, extra=self.properties)
            else:
                raise Exception("error_type not understood")

    def exception(self):
        """ Send an Exception
        try:
            result = 1 / 0  # generate a ZeroDivisionError
        except Exception:
            logger.exception()
        """
        if self.properties is None:
            self.logger.exception('Exception.', extra=self.properties)
        else:
            self.logger.exception('Exception.')
