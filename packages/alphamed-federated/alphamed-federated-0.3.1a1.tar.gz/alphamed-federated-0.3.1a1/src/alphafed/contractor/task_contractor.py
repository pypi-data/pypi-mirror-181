"""Tools for task related contracts."""

from io import IOBase
import os
from typing import List, Optional, overload

import requests

from .. import logger
from .common import ContractException, Contractor

__all__ = ['TaskContractor', 'AutoTaskContractor']


class TaskContractor(Contractor):
    """A contractor to handle task related ones."""

    _URL = 'http://federated-service:9080/fed-service/api/v2'

    _BASE_DATA_DIR = '/data/alphamed-federated'

    def __init__(self, task_id: str) -> None:
        super().__init__()
        self.task_id = task_id

    def _validate_response(self, resp: requests.Response) -> dict:
        if resp.status_code < 200 or resp.status_code >= 300:
            raise ContractException(f'failed to submit a contract: {resp}')
        resp_json: dict = resp.json()
        if not resp_json or not isinstance(resp_json, dict):
            raise ContractException(f'invalid response:\nresp: {resp}\njson: {resp_json}')
        if resp_json.get('code') != 0:
            raise ContractException(f'failed to handle a contract: {resp_json}')
        data = resp_json.get('data')
        if data is None or not isinstance(data, dict):
            raise ContractException(f'contract data error: {resp_json}')
        task_id = data.get('task_id')
        assert task_id is None or task_id == self.task_id, f'task_id dismatch: {task_id}'
        return data

    def query_address(self, target: str) -> Optional[str]:
        """Query address of the target."""
        assert target and isinstance(target, str), f'invalid target node: {target}'
        post_data = {
            'task_id': self.task_id,
            'node_id': target
        }
        post_url = f'{self._URL}/fed/network/node/detail'
        resp = requests.post(url=post_url, json=post_data, headers=self._HEADERS)
        resp_data = self._validate_response(resp=resp)
        ip = resp_data.get('node_ip')
        if not ip or not isinstance(ip, str):
            logger.warn(f'failed to obtain target address: {resp_data}')
            return None
        else:
            return ip

    def query_nodes(self) -> List[str]:
        """Query all nodes in this task."""
        task_type_manual = 1
        post_data = {
            'task_id': self.task_id,
            'task_type': task_type_manual
        }
        post_url = f'{self._URL}/task/nodelist'
        resp = requests.post(url=post_url, json=post_data, headers=self._HEADERS)
        resp_data = self._validate_response(resp=resp)
        records: list[dict] = resp_data.get('records')
        assert (
            records and isinstance(records, list)
        ), f'failed to query node IDs of task: {self.task_id}'
        for _node in records:
            assert _node and _node.get('node_id'), f'broken node data: {records}'
        return [_node['node_id'] for _node in records]

    @overload
    def upload_file(self, fp: str, persistent: bool = False, upload_name: str = None) -> str: ...

    @overload
    def upload_file(self, fp: IOBase, persistent: bool = False, upload_name: str = None) -> str: ...

    def upload_file(self, fp, persistent: bool = False, upload_name: str = None) -> str:
        """Upload a file to file system."""
        assert fp, 'nothing to upload'
        assert isinstance(fp, (str, IOBase)), f'invalid file type: {type(fp)}'
        if isinstance(fp, str):
            assert (
                isinstance(fp, str) and os.path.isfile(fp)
            ), f'{fp} does not exist or is not a file'

        post_data = {
            'task_id': self.task_id,
            'durable': persistent
        }
        post_url = f'{self._URL}/file/upload'
        headers = self._HEADERS.copy()
        headers.pop('content-type')  # use form-data rather than json data
        if isinstance(fp, str):
            post_data['file_path'] = fp
            resp = requests.post(url=post_url, params=post_data, headers=headers)
            logger.error(f'{post_data=}')
            logger.error(f'{resp=}')
        else:
            post_data['file_path'] = upload_name
            fp.seek(0)
            files = [('files', fp)]
            resp = requests.post(url=post_url, params=post_data, headers=headers, files=files)
        resp_data = self._validate_response(resp=resp)
        file_url = resp_data.get('f_url')
        assert file_url and isinstance(file_url, str), f'Invalid file url: `{file_url}`.'
        return file_url

    def report_progress(self, percent: int) -> None:
        """Report training progress (percent integer value)."""
        assert (
            isinstance(percent, int) and 0 <= percent and percent <= 100
        ), f'Invalid progress value: {percent}.'

        post_data = {
            'task_id': self.task_id,
            'progress_number': percent
        }
        post_url = f'{self._URL}/automl/task/progress'
        resp = requests.post(url=post_url, json=post_data, headers=self._HEADERS)
        self._validate_response(resp=resp)


class AutoTaskContractor(TaskContractor):
    """AutoML version TaskContractor."""

    def query_nodes(self) -> List[str]:
        """Query all nodes in this task."""
        task_type_auto_ml = 2
        post_data = {
            'task_id': self.task_id,
            'task_type': task_type_auto_ml
        }
        post_url = f'{self._URL}/task/nodelist'
        resp = requests.post(url=post_url, json=post_data, headers=self._HEADERS)
        resp_data = self._validate_response(resp=resp)
        records: list[dict] = resp_data.get('records')
        assert (
            records and isinstance(records, list)
        ), f'failed to query node IDs of task: {self.task_id}'
        for _node in records:
            assert _node and _node.get('node_id'), f'broken node data: {records}'
        return [_node['node_id'] for _node in records]
