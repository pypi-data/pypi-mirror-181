from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.v1_task_get_by_status_and_workspace_response_200_tasks_item import \
    V1TaskGetByStatusAndWorkspaceResponse200TasksItem

T = TypeVar("T", bound="V1TaskGetByStatusAndWorkspaceResponse200")

@attr.s(auto_attribs=True)
class V1TaskGetByStatusAndWorkspaceResponse200:
    """ Response body of /tasks/get_by_status_and_workspace

    Attributes:
        tasks (List[V1TaskGetByStatusAndWorkspaceResponse200TasksItem]):  A list of tasks matching the specified status
            and workspace.
    """

    tasks: List[V1TaskGetByStatusAndWorkspaceResponse200TasksItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self.tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "tasks": tasks,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tasks = []
        _tasks = d.pop("tasks")
        for tasks_item_data in (_tasks):
            tasks_item = V1TaskGetByStatusAndWorkspaceResponse200TasksItem.from_dict(tasks_item_data)



            tasks.append(tasks_item)


        v1_task_get_by_status_and_workspace_response_200 = cls(
            tasks=tasks,
        )

        v1_task_get_by_status_and_workspace_response_200.additional_properties = d
        return v1_task_get_by_status_and_workspace_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
