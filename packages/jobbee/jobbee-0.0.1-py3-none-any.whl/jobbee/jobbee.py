import logging

import requests


logger = logging.getLogger(__name__)

API_VERSION = 'v0'


class JobBee(object):
    """
    Represents a Job Bee in the system.
    """

    def __init__(self, user_id=None, url='http://localhost', api_key=None, id=None):
        """
        Params:
        -------
        user_id: str
            Your Job Bee user id.
        url: str
            The URL of the Job Bee server.
        api_key: str
            The API key to use for authentication against the Job Bee server.
        id: str,
            The ID of the Job Bee that you want to work with.
        """
        self.user_id = user_id
        self.url = url
        self.api_key = api_key
        self.id = id

        logger.debug(f'Job Bee API base URL: {self.url}')

        self.access_token = None
        self.run_id = None
        self._status = 'idle'
        self._stage = 0

    def check_connection(self) -> bool:
        """
        Checks that the connection to the Job Bee API is working correctly.

        Returns:
        --------
        bool:
            True if the connection to Job Bee is working correctly.
        """
        logger.info('Checking connection to Job Bee API...')

        if self.url is None:
            logger.error('No URL provided. Have you forgotten to set the URL?')
            return False

        url = f'{self.url}/{API_VERSION}/jobbee/{self.id}/check'
        headers = {
            'x-api-key': self.api_key,
        }
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return True
            logger.debug(r.status_code)
            logger.debug(r.text)
        except requests.exceptions.ConnectionError:
            logger.error(
                'Unable to connect to the Job Bee API. Please check your config.')

        return False

    def start_run(self):
        """
        Triggers the running of a new instance of the Job Bee.
        """
        logger.info('Starting run for job bee...')

        if self.url is None:
            logger.error('No URL provided. Have you forgotten to set the URL?')
            return False

        url = f'{self.url}/{API_VERSION}/jobbee/{self.id}/start'
        headers = {
            'x-api-key': self.api_key,
        }
        try:
            r = requests.post(url, headers=headers)
            if r.status_code == 200:
                logger.debug(r.text)
                result = r.json()
                self.run_id = result['run']
                self._status = 'running'
                return True
            logger.debug(r.status_code)
            logger.debug(r.text)
        except requests.exceptions.ConnectionError:
            logger.error(
                'Unable to connect to the Job Bee API. Please check your config.')

        return False

    def end_run(self, success=False):
        """
        Ends the running of a Job Bee instance.

        Params:
        -------
        success: bool
            Whether the Job Bee run was successful.
        """
        pass

    def status(self) -> str:
        """
        Gets the status of the Job Bee instance.
        """
        return f'status={self._status}, stage={self._stage}'

    def stage_start(self) -> bool:
        """
        Mark the current stage of the Job Bee instance as started.

        Returns:
        -------
        bool:
            Whether the call to the Job Bee server was successful.

        """
        logger.info('Reporting stage start...')

        if self.url is None:
            logger.error('No URL provided. Have you forgotten to set the URL?')
            return False

        url = f'{self.url}/{API_VERSION}/report/{self.id}/run/{self.run_id}/stage/{self._stage}/started'
        headers = {
            'x-api-key': self.api_key,
        }
        try:
            r = requests.post(url, headers=headers)
            if r.status_code == 201:
                return True
        except requests.exceptions.ConnectionError:
            logger.error(
                'Unable to connect to the Job Bee API. Please check your config.')

        return False

    def stage_end(self):
        """
        Mark the current stage of the Job Bee instance as stopped.

        Returns:
        -------
        bool:
            Whether the call to the Job Bee server was successful.

        """
        logger.info('Reporting stage ended...')

        if self.url is None:
            logger.error('No URL provided. Have you forgotten to set the URL?')
            return False

        url = f'{self.url}/{API_VERSION}/report/{self.id}/run/{self.run_id}/stage/{self._stage}/stopped'
        headers = {
            'x-api-key': self.api_key,
        }
        try:
            r = requests.post(url, headers=headers)
            if r.status_code == 201:
                self._stage += 1
                return True
        except requests.exceptions.ConnectionError:
            logger.error(
                'Unable to connect to the Job Bee API. Please check your config.')

    def stage_failed(self, message=None):
        """
        Mark the current stage of the Job Bee instance as failed.

        Returns:
        -------
        bool:
            Whether the call to the Job Bee server was successful.

        """
        logger.info('Reporting stage failed...')

        if self.url is None:
            logger.error('No URL provided. Have you forgotten to set the URL?')
            return False

        url = f'{self.url}/{API_VERSION}/report/{self.id}/run/{self.run_id}/stage/{self._stage}/failed'
        headers = {
            'x-api-key': self.api_key,
        }
        try:
            payload = {
                'message': message,
            }
            r = requests.post(url, headers=headers, json=payload)
            if r.status_code == 201:
                self._stage += 1
                return True
        except requests.exceptions.ConnectionError:
            logger.error(
                'Unable to connect to the Job Bee API. Please check your config.')
