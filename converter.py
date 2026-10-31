"""Convert Excel binary workbooks (.xlsb) to .xlsx."""
from pathlib import Path

from openpyxl import Workbook
from python_calamine import CalamineWorkbook


def convert(source: Path, target: Path) -> None:
    """Copy every sheet's values from `source` into a new workbook at `target`."""
    reader = CalamineWorkbook.from_path(str(source))
    writer = Workbook(write_only=True)
    for name in reader.sheet_names:
        sheet = writer.create_sheet(title=name)
        for row in reader.get_sheet_by_name(name).to_python(skip_empty_area=False):
            sheet.append([None if cell == "" else cell for cell in row])
    writer.save(target)
