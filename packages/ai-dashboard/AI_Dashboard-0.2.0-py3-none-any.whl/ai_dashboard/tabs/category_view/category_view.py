from typing import Optional, Dict, Any

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

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(endpoints)

        if config is not None:
            self._config = config
        else:
            self.reset()
