import os
import shutil
import zipfile


class UnpackKerasArchiveMixin:
    def _unpack_archive_if_needed(self, path: str) -> None:
        if not zipfile.is_zipfile(path):
            return

        with zipfile.ZipFile(path, "r") as zip_ref:
            if ".zip" in path:
                path = path.replace(".zip", "")

            tmp_path = f"{path}-tmp"
            zip_ref.extractall(tmp_path)

            os.remove(path)  # we remove zip archive to place the extracted files in its place

            shutil.move(tmp_path, path)

            archive_inners = os.listdir(path)
            if len(archive_inners) == 1:  # that means that the whole model folder was archived instead of just inner files
                inner_path = os.path.join(path, archive_inners[0])

                shutil.move(inner_path, tmp_path)
                os.rmdir(path)
                shutil.move(tmp_path, path)
