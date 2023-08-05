__version__ = "1.7.4"

import logging
from urllib.parse import urlparse, parse_qs
import dateutil.parser
import requests

logger = logging.getLogger(__name__)


class QRonosError(Exception):
    """Generic exception for QRonos"""
    def __init__(self, msg):
        super().__init__()
        logger.error(f"[QRONOS API] - {msg}")


class QRonosClient(object):
    urls = {}
    headers = {}

    def __init__(self, host, token=None, verify=True):
        host = urlparse(host, scheme='https').geturl().rstrip('/')
        self._set_urls(host)
        self.verify = verify
        if token:
            self._set_headers(token)

    def _set_headers(self, token):
        self.headers = {"Authorization": f"Token {token}"}

    def _set_urls(self, host):
        prefix = f"{host}/api"
        self.urls = {
            'login': f"{prefix}/login/",
            'logout': f"{prefix}/logout/",
            'logoutall': f"{prefix}/logoutall/",
            'import_status': f"{prefix}/import_status/",
            'tracker_import': f"{prefix}/tracker_import/",
            'stage_import': f"{prefix}/stage_import/",
            'delete_items': f"{prefix}/delete_items/",
            'get_attributes': f"{prefix}/attributes/",
            'get_stages': f"{prefix}/stages/",
            'get_stage_history': f"{prefix}/stage_history/",
            'get_attribute_history': f"{prefix}/attribute_history/",
        }

    def _get(self, *args, **kwargs):
        if self.headers:
            kwargs.setdefault("headers", {}).update(self.headers)
        try:
            return requests.get(*args, verify=self.verify, **kwargs)
        except requests.exceptions.RequestException as err:
            raise QRonosError("Unable to connect") from err

    def _post(self, *args, **kwargs):
        if self.headers:
            kwargs.setdefault("headers", {}).update(self.headers)
        try:
            return requests.post(*args, verify=self.verify, **kwargs)
        except requests.exceptions.RequestException as err:
            raise QRonosError("Unable to connect") from err

    def login(self, username, password):
        """Login and fetch token"""
        response = self._post(self.urls['login'], data={'username': username, 'password': password})
        if not response.status_code == 200:
            raise QRonosError("Invalid credentials")
        try:
            response_json = response.json()
            token, expiry = response_json["token"], dateutil.parser.parse(response_json["expiry"])
        except Exception as err:
            raise QRonosError("Unable to get token") from err
        self._set_headers(token)
        return token, expiry

    def logout(self, all_tokens=False):
        """Logout (optionally to remove all tokens)"""
        logout_url = self.urls['logoutall'] if all_tokens else self.urls['logout']
        response = self._post(logout_url)
        if response.status_code == 204:
            return True
        raise QRonosError("Unable to logout")

    def import_status(self, job_id):
        """Get the status of an import"""
        response = self._get(self.urls['import_status'], params={'job_id': job_id})
        if response.status_code == 200:
            try:
                return response.json()["status"]
            except Exception as err:
                raise QRonosError("Unable to get status") from err
        elif response.status_code == 404:
            raise QRonosError(response.json()["job_id"])
        else:
            raise QRonosError(f"Bad Request - {response.status_code} - {response.reason}")

    def _run_import(self, url, post_data):
        """Helper function to post import and handle response"""
        response = self._post(url, json=post_data)
        if response.status_code == 202:
            try:
                return response.json()["job_id"]
            except Exception as err:
                raise QRonosError("Unable to get Job ID from Import request") from err
        raise QRonosError(f"Bad Import request - {response.content}")

    def tracker_import(self, tracker_id, unique_columns, can_add_item, can_delete_item, data, extra_column_name=None):
        """
        Imports tracker (item) data.

        :param tracker_id: The ID of the Tracker
        :param unique_columns: A list of the header fields
        :param can_add_item: Import can add Items?
        :param can_delete_item: Import can delete Items?
        :param data: The import data as a list of dictionaries (keys must match the headers from unique_columns parameter)
        :param extra_column_name When provided this header will serve as an extra source of data for the items
        :return: Job ID
        """
        body = {
            'tracker': tracker_id,
            'unique_columns': unique_columns,
            'can_add_item': can_add_item,
            'can_delete_item': can_delete_item,
            'data': data,
        }
        if extra_column_name:
            body['extra_column_name'] = extra_column_name
        return self._run_import(
            self.urls['tracker_import'],
            body
        )

    def stage_import(self, stage_id=None, tracker_stage_id=None, data=None):
        """
        Imports stage data.

        :param stage_id: The ID of the Stage
        :param tracker_stage_id: The ID of the Tracker Stage
        :param data: The import data as a list of dictionaries (keys must match names in QRonos)
        :return: Job ID
        """
        post_data = {'data': data}
        if stage_id:
            post_data.update({'stage': stage_id})
        elif tracker_stage_id:
            post_data.update({'tracker_stage': tracker_stage_id})
        elif stage_id and tracker_stage_id:
            raise QRonosError("You can't provide both a stage_id and a tracker_stage_id")
        else:
            raise QRonosError("Provide either a stage_id or a tracker_stage_id")
        
        return self._run_import(
            self.urls['stage_import'],
            post_data
        )

    def delete_items(self, tracker_id, data):
        """
        Deletes Items from a Tracker

        :param tracker_id: The ID of the Tracker
        :param data: A list of the unique keys you wish to delete
        :return: Job ID
        """
        return self._run_import(
            self.urls['delete_items'],
            {
                'tracker': tracker_id,
                'data': data
            }
        )

    def get_item_attributes(
        self, 
        show_mastered=True, 
        show_non_mastered=True, 
        tracker=None, 
        unique_keys=None, 
        unique_key=None,
        page_size=None,
        page=None,
    ):
        """
        Get item attributes with a tracker ID or using a unique key(s)

        Keyword arguments:
            :param show_mastered: Include mastered attributes
            :param show_non_mastered: Include non-mastered attributes
            :param tracker: The ID of the Tracker
            :param unique_keys: A list of unique item keys
            :param unique_key: A unique item key 
            :param page_size: Number of items per page
            :param page: The link for next page
        :return: Item attributes
        """

        post_data = {
            "show_mastered": show_mastered,
            "show_non_mastered": show_non_mastered,
        }
        params = {}

        if tracker:
            post_data["tracker"] = tracker
        if unique_keys:
            post_data["unique_keys"] = unique_keys
        elif unique_key:
            post_data["unique_key"] = unique_key
        if page:
            params.update(parse_qs(urlparse(page).query))
        if page_size:
            params['page_size'] = page_size

        response = self._post(self.urls['get_attributes'], json=post_data, params=params)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as err:
                raise QRonosError("Unable to get attribute data") from err
        else:
            raise QRonosError(f"QRONOS Error - {response.status_code} - {response.reason}")

    def get_item_stages(
        self, 
        tracker=None, 
        unique_keys=None, 
        unique_key=None, 
        stages=None, 
        stage=None,
        tracker_stage=None,
        tracker_stages=None,
        page_size=None,
        page=None,
    ):
        """
        Get item stages with a tracker ID or using a unique key(s) which can be restricted by stage(s)

        Keyword arguments:
            :param tracker: The ID of the Tracker
            :param unique_keys: A list of unique item keys
            :param unique_key: A unique item key
            :param stages: A list of stage ids (Stage model)
            :param stage: The ID of a stage (Stage model)
            :param tracker_stage: The ID of a tracker stage (TrackerStage model)
            :param tracker_stages: A list of tracker stage ids (TrackerStage model)
            :param page_size: Number of items per page
            :param page: The link for next page
        :return: Item stages
        """

        post_data = {}
        params = {}

        if tracker:
            post_data["tracker"] = tracker
        if unique_keys:
            post_data["unique_keys"] = unique_keys
        elif unique_key:
            post_data["unique_key"] = unique_key

        if stages:
            post_data["stages"] = stages
        elif stage:
            post_data["stage"] = stage
        elif tracker_stage:
            post_data["tracker_stage"] = tracker_stage
        elif tracker_stages:
            post_data["tracker_stages"] = tracker_stages

        if page:
            params.update(parse_qs(urlparse(page).query))
        if page_size:
            params['page_size'] = page_size

        response = self._post(self.urls['get_stages'], json=post_data, params=params)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as err:
                raise QRonosError("Unable to get stage data") from err
        else:
            raise QRonosError(f"QRONOS Error - {response.status_code} - {response.reason}")

    def get_item_stage_history(
            self,
            tracker=None,
            unique_keys=None,
            unique_key=None,
            stages=None,
            stage=None,
            tracker_stage=None,
            tracker_stages=None,
            interval_start_date=None,
            interval_end_date=None,
            fields=None,
            page_size=None,
            page=None,
    ):

        """
        Get item stages history with a tracker ID or using a unique key(s) which can be restricted by stage(s)

        Keyword arguments:
            :param tracker: The ID of the Tracker
            :param unique_keys: A list of unique item keys
            :param unique_key: A unique item key
            :param stages: A list of stage ids (Stage model)
            :param stage: The ID of a stage (Stage model)
            :param tracker_stage: The ID of a tracker stage (TrackerStage model)
            :param tracker_stages: A list of tracker stage ids (TrackerStage model)
            :param interval_start_date: Date beginning for time period to fetch history in iso-8601 format
            :param interval_end_date: Date end for time period to fetch history in iso-8601 format
            :param fields: A list of  attributes names of ItemStage
            :param page_size: Number of items per page
            :param page: The link for next page
        :return: Item stages history
        """

        post_data = {}
        params = {}

        if tracker:
            post_data["tracker"] = tracker
        if unique_keys:
            post_data["unique_keys"] = unique_keys
        elif unique_key:
            post_data["unique_key"] = unique_key

        if stages:
            post_data["stages"] = stages
        elif stage:
            post_data["stage"] = stage
        elif tracker_stage:
            post_data["tracker_stage"] = tracker_stage
        elif tracker_stages:
            post_data["tracker_stages"] = tracker_stages

        if interval_start_date:
            post_data["interval_start_date"] = interval_start_date
        if interval_end_date:
            post_data["interval_end_date"] = interval_end_date

        if fields:
            post_data["fields"] = fields

        if page:
            params.update(parse_qs(urlparse(page).query))
        if page_size:
            params['page_size'] = page_size

        response = self._post(self.urls['get_stage_history'], json=post_data, params=params)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as err:
                raise QRonosError("Unable to get stage history data") from err
        else:
            raise QRonosError(f"QRONOS Error - {response.status_code} - {response.reason}")

    def get_all_item_attributes(self, **kwargs):
        """
        Get all item attributes with a tracker ID or using a unique key(s)

        Keyword arguments:
            :param show_mastered: Include mastered attributes
            :param show_non_mastered: Include non-mastered attributes
            :param tracker: The ID of the Tracker
            :param unique_keys: A list of unique item keys
            :param unique_key: A unique item key
            :param page_size: Number of items per iteration
        :return: Item attributes
        """
        return self._get_all_item_data(get_data_method=self.get_item_attributes, **kwargs)

    def get_all_item_stages(self, **kwargs):
        """
        Get all item stages with a tracker ID or using a unique key(s) which can be restricted by stage(s)

        Keyword arguments:
            :param tracker: The ID of the Tracker
            :param unique_keys: A list of unique item keys
            :param unique_key: A unique item key
            :param stages: A list of stage ids (Stage model)
            :param stage: The ID of a stage (Stage model)
            :param tracker_stage: The ID of a tracker stage (TrackerStage model)
            :param tracker_stages: A list of tracker stage ids (TrackerStage model)
            :param page_size: Number of items retrieved per iteration
        :return: Item stages
        """
        return self._get_all_item_data(get_data_method=self.get_item_stages, **kwargs)

    def get_all_item_stage_history(self, **kwargs):
        """
        Get all item stages history with a tracker ID or using a unique key(s) which can be restricted by stage(s)

        Keyword arguments:
            :param tracker: The ID of the Tracker
            :param unique_keys: A list of unique item keys
            :param unique_key: A unique item key
            :param stages: A list of stage ids (Stage model)
            :param stage: The ID of a stage (Stage model)
            :param tracker_stage: The ID of a tracker stage (TrackerStage model)
            :param tracker_stages: A list of tracker stage ids (TrackerStage model)
            :param page_size: Number of retrieved per iteration
        :return: Item stages history
        """
        return self._get_all_item_data(get_data_method=self.get_item_stage_history, **kwargs)

    def get_all_item_attribute_history(self, **kwargs):
        """
        Get all item attribute history with a tracker ID with optional unique key(s)

        Keyword arguments:
        :param tracker: The ID of the Tracker
        :param unique_keys: A list of unique item keys
        :param unique_key: A unique item key
        :param attribute_names: a list of attribute input names
        :param page_size: Number of retrieved per iteration
        :return: Item stages history
        """
        return self._get_all_item_data(get_data_method=self.get_item_attribute_history, **kwargs)

    @staticmethod
    def _get_all_item_data(get_data_method, **kwargs):
        """
        loops through and aggregates all pages for a given qronos client get_data method given the appropriate kwargs
        Keyword arguments:
            :param get_data_method: A qronos client get_data method
        :return: all pages for given get method
        """

        # Need to remove page from kwargs so that it doesn't overwrite when calling get_data_method
        kwargs.pop("page", None)

        all_data = []
        data = get_data_method(**kwargs)
        all_data.extend(data.get('items'))
        while nextp := data.get('next'):
            data = get_data_method(page=nextp, **kwargs)
            all_data.extend(data.get('items'))
        return all_data

    def get_item_attribute_history(
        self,
        tracker=None,
        attribute_names=None,
        unique_keys=None,
        unique_key=None,
        page_size=None,
        page=None,
    ):
        """
        Get item attribute history with a tracker ID with optional unique key(s)

        Keyword arguments:
        :param tracker: The ID of the Tracker
        :param attribute_names: A list of attribute input names
        :param unique_keys: A list of unique item keys
        :param unique_key: A unique item key
        :param page_size: Number of retrieved per iteration
        :param page: The link for next page
        :return: Item attribute history
        """

        post_data = {
            "tracker": tracker,
            "attribute_names": attribute_names
        }
        params = {}

        if unique_keys:
            post_data["unique_keys"] = unique_keys
        elif unique_key:
            post_data["unique_key"] = unique_key

        if page:
            params.update(parse_qs(urlparse(page).query))
        if page_size:
            params['page_size'] = page_size

        response = self._post(self.urls['get_attribute_history'], json=post_data, params=params)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as err:
                raise QRonosError("Unable to get attribute history data") from err
        else:
            raise QRonosError(f"QRONOS Error - {response.status_code} - {response.reason}")
