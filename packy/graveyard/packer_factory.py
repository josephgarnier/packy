"""
Copyright 2023-present, Marie-Neige Chapel
All rights reserved.

See LICENCE.md file for more information.
"""

# PackY
from packy.graveyard.task_list_model import TaskListModel
from packy.graveyard.zip_packer import ZipPacker


# -----------------------------------------------------------------------------
def createPacker(task: TaskListModel):
    extension = task.packerData().extension()

    match extension:
        case "zip" | "lzma":
            return ZipPacker(task)
        case _:
            raise Exception("[createPacker] extension not recognized.")
