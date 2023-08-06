from typing import Optional, Dict, Any

from ai_dashboard.api import endpoints
from ai_dashboard.tabs import abstract_tab


class CategoryView(abstract_tab.Tab):
    ID = "CLUSTER_VIEW"

    BLANK: Dict[str, Any] = {
        "activeFilterGroup": "",
        "color": None,
        "configuration": {},
        "name": "",
        "type": ID,
    }

    def __init__(
        self,
        endpoints: endpoints.Endpoints,
        dataset_id: str,
        title: Optional[str] = None,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()

        self._endpoints = endpoints

        if config is not None:
            self._config = config
        else:
            self.reset()

        self.dataset_id = dataset_id
        self.config["colour"] = colour
        self.config["configuration"]["title"] = self.ID if title is None else title
        self.config["name"] = name

    @classmethod
    def from_fields(
        cls,
        primary_field: str,
        secondary_field: str,
        cluster_field: str = "userImage",
        subcluster_field: str = "",
        layout_template: str = "custom",
        title: Optional[str] = None,
        name: Optional[str] = None,
        colour: Optional[str] = None,
    ):
        category_view = cls(name=name, title=title, colour=colour)
        category_view.config = {
            "activeFilterGroup": "",
            "color": colour,
            "configuration": {
                "previewDocumentCardConfiguration": {
                    "layoutTemplateConfiguration": {
                        "fields": [
                            {
                                "id": "primary",
                                "value": primary_field,
                            },
                            {
                                "id": "secondary",
                                "value": secondary_field,
                            },
                        ]
                    },
                    "layoutTemplate": layout_template,
                },
                "subclusterField": subcluster_field,
                "clusterField": cluster_field,
            },
            "name": name,
            "type": cls.ID,
        }
        return category_view

    def set_view(
        self,
        primary_field: str,
        secondary_field: str = None,
        cluster_field: str = "userImage",
        subcluster_field: str = "",
        layout_template: str = "custom",
    ):
        self.config["configuration"] = {
            "previewDocumentCardConfiguration": {
                "layoutTemplateConfiguration": {"fields": []},
                "layoutTemplate": layout_template,
            },
            "subclusterField": subcluster_field,
            "clusterField": cluster_field,
        }
        if primary_field is not None:
            self.config["configuration"]["previewDocumentCardConfiguration"][
                "layoutTemplateConfiguration"
            ]["fields"].append(
                {
                    "id": "primary",
                    "value": primary_field,
                }
            )
        if secondary_field is not None:
            self.config["configuration"]["previewDocumentCardConfiguration"][
                "layoutTemplateConfiguration"
            ]["fields"].append(
                {
                    "id": "secondary",
                    "value": secondary_field,
                }
            )
