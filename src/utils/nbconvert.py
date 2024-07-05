"""Collection of nbconvert preprocessors."""

import re
from nbconvert.preprocessors import Preprocessor


class HtmlPuzzlePathPreprocessor(Preprocessor):
    """
    Preprocessor which changes notebook puzzle links to HTML links for cells
    tagged as 'catalogue'.
    """
    def preprocess_cell(self, cell, resources, index):
        """Preprocess a cell."""
        if (
            cell.cell_type == "code" and
            "tags" in cell.metadata and "catalogue" in cell.metadata.tags
        ):
            for idx, output in enumerate(cell.outputs):
                cell.outputs[idx]["data"]["text/html"] = re.sub(
                    r"aoc(\d+)_day(\d+)_(\d+).ipynb", r"aoc\1_day\2_\3.html",
                    output["data"]["text/html"]
                )
        return cell, resources
