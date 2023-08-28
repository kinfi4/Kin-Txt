import os
import shutil
import zipfile


class UnpackArchiveMixin:
    def _unpack_archive_if_needed(self, path: str) -> None:
        if not zipfile.is_zipfile(path):
            return

        with zipfile.ZipFile(path, "r") as zip_ref:
            if ".zip" in path:
                new_model_path = path.replace(".zip", "")
                zip_ref.extractall(new_model_path)

                os.remove(path)
            else:
                tmp_path = f"{path}-tmp"
                zip_ref.extractall(tmp_path)
                os.remove(path)
                shutil.move(tmp_path, path)
