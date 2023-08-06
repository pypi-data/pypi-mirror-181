from typing import Optional
import logging


from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase, Undefined

from .base_handler import BaseHandler

logger = logging.getLogger('factro_client')

@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class Task:
    id: str
    mandant_id: str
    number: int
    custom_fields: Optional[dict]
    change_date: Optional[str] = ''
    creator_id: Optional[str] = ''
    title: Optional[str] = ''
    officer_id: Optional[str] = ''
    planned_effort: Optional[float] = 0.0
    project_id: Optional[str] = ''
    realized_effort: Optional[float] = 0.0
    remaining_effort: Optional[float] = 0.0
    executor_id: Optional[str] = ''
    is_milestone: Optional[bool] = False
    task_state: Optional[str] = ''
    parent_package_id: str = None
    company_contact_id: Optional[str] = ''
    description: Optional[str] = ''
    end_date: Optional[str] = ''
    start_date: Optional[str] = ''
    company_id: Optional[str] = ''
    paused_until: Optional[str] = ''
    task_priority: Optional[int] = 0


class TaskHandler(BaseHandler):

    def __init__(self, url: str, api_key: str):
        super(TaskHandler, self).__init__(url, api_key)

    def get_task_by_id(self, task_id) -> Task:
        path = f"/api/core/tasks/{task_id}"

        json_data = self.do_get(path)

        logger.debug(f"TaskHandler.get_task_by_id({task_id} -> {json_data}")
        try:
            task = Task.schema().load(json_data)
        except Exception as e:
            logger.error(f"TaskHandler.get_task_by_id({task_id} -> {json_data})")
            raise e

        return task