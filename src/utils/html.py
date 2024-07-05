"""Collection of HTML utility functions."""

from collections import UserDict
from IPython.display import HTML, display


class HtmlAttributes(UserDict):
    """Dictionary of HTML attributes."""
    def __init__(self, mapping=None):
        if mapping is None:
            mapping = {}
        super().__init__(mapping)
        self.changed = False

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.changed = True

    def __delitem__(self, key):
        super().__delitem__(key)
        self.changed = True

    def __repr__(self):
        return ' '.join([f"{key}=\"{value}\"" for key, value in self.items()])


class HtmlElement:
    """HTML element."""
    # pylint: disable=R0903
    def __init__(self, tag_name, content=None, attributes=HtmlAttributes()):
        self.tag_name = tag_name
        self.content = (
            "".join(map(str, content))
            if hasattr(content, '__iter__') else content
        )
        self.attributes = attributes

    def __repr__(self):
        if self.content is None:  # element with self-closing tag
            return f"<{self.tag_name} {self.attributes}/>"
        return (
            f"<{self.tag_name} {self.attributes}>"
            f"{self.content}"
            f"</{self.tag_name}>"
        )


class CatalogueTag(HtmlElement):
    """Tag of an AOC catalogue."""
    # pylint: disable=R0903,C0415
    def __init__(self, tag_type):
        from .icons import FontAwesomeIcon

        tag_subtype = ""
        if isinstance(tag_type, tuple):
            tag_type, tag_subtype = tag_type[0], f"({tag_type[1]})"
        attributes = HtmlAttributes({"style": "display: inline-block;"})
        icon_name = {
            "algorithmics": "microchip",
            "data structure": "diagram_project",
            "fundamentals": "shapes",
            "image processing": "image",
            "interpretation": "language",
            "optimization": "rocket",
            "analysis": "chart_simple",
            "simulation": "clapperboard",
            "misc": "star",
            "highlight": "heart"
        }[tag_type]
        icon = FontAwesomeIcon(
            icon_name,
            tag_type,
            HtmlAttributes({
                "align": "left",
                "style": "height: 15px; vertical-align: middle; "
                         "margin: 0px 5px 0px 0px;"
            })
        )
        content = [icon, tag_subtype]
        super().__init__("div", content, attributes)


class CatalogueBadge(HtmlElement):
    """Badge of an AOC catalogue."""
    # pylint: disable=R0903,C0415
    def __init__(self, badge_name):
        from .icons import ShieldsIoIcon
        attributes = HtmlAttributes({"style": "display: inline-block;"})
        width = f"{(102 if badge_name == 'Pylint' else 136) * 0.7}px"
        icon = ShieldsIoIcon(
            badge_name,
            badge_name,
            HtmlAttributes({
                "align": "left",
                "style": f"height: 15px; width: {width}; "
                         "vertical-align: middle; margin: 0px 5px 0px 0px;"
            })
        )
        super().__init__("div", icon, attributes)


class CatalogueRow(HtmlElement):
    """Row of an AOC catalogue."""
    # pylint: disable=R0903,R0913
    def __init__(
        self, day, part, puzzle_name, tag_types, difficulty, badges, href
    ):
        cell_attributes = HtmlAttributes({"style": "text-align: left;"})
        hidden_cell_attributes = HtmlAttributes({"style": "display: none"})
        content = [
            HtmlElement(
                "td", day,
                cell_attributes if day is not None else hidden_cell_attributes
            ),
            HtmlElement(
                "td", part,
                cell_attributes if part is not None else hidden_cell_attributes
            ),
            HtmlElement(
                "td", HtmlElement(
                    "a", f"{puzzle_name}", HtmlAttributes(
                        {"href": href, "target": "_blank"}
                    )
                ),
                cell_attributes if puzzle_name is not None
                else hidden_cell_attributes
            ),
            HtmlElement(
                "td", "&nbsp;&nbsp;".join([
                    str(CatalogueTag(tag_type))
                    for tag_type in (tag_types or [])
                ]),
                cell_attributes if tag_types is not None
                else hidden_cell_attributes
            ),
            HtmlElement(
                "td", difficulty,
                cell_attributes if difficulty is not None
                else hidden_cell_attributes
            ),
            HtmlElement(
                "td", "&nbsp;&nbsp;".join([
                    str(CatalogueBadge(badge))
                    for badge in (badges or [])
                ]),
                cell_attributes if badges is not None
                else hidden_cell_attributes
            )
        ]
        super().__init__("tr", content)


class CatalogueTable(HtmlElement):
    """HTML table representing the AOC catalogue."""
    # pylint: disable=R0903
    def __init__(
        self, header, data,
        puzzle_dir_pattern="./2022/aoc2022_day{0}_{1}.ipynb",
        hide_odd_row_days=True
    ):
        show_column = [width not in ("0", "0px") for _, width in header]
        header = HtmlElement("tr", [
            HtmlElement(
                "th", title, HtmlAttributes({
                    "style": f"width: {width}; text-align: left;"
                    if width not in ("0", "0px") else "display: none"
                })
            )
            for title, width in header
        ])
        rows = []
        for row_index, (
            day, part, puzzle_name, tag_types, difficulty, badges
        ) in enumerate(data):
            rows.append(
                CatalogueRow(
                    ((
                        day
                        if not hide_odd_row_days or row_index % 2 != 1 else ""
                    )) if show_column[0] else None,
                    part if show_column[1] else None,
                    puzzle_name if show_column[2] else None,
                    tag_types if show_column[3] else None,
                    difficulty if show_column[4] else None,
                    badges if show_column[5] else None,
                    puzzle_dir_pattern.format(day, part)
                )
            )
        content = [header, *rows]
        super().__init__(
            "table", content, HtmlAttributes({"style": "width: 100%;"})
        )

    def display(self):
        """Display catalogue table in IPython notebook."""
        display(HTML(str(self)))


class TagTable(HtmlElement):
    """HTML table representing the AOC tag table."""
    # pylint: disable=R0903,C0415
    def __init__(self, header, data):
        from .icons import FontAwesomeIcon

        header = HtmlElement("tr", [
            HtmlElement(
                "th", title, HtmlAttributes(
                    {"style": f"width: {width}; text-align: left;"}
                )
            )
            for title, width in header
        ])
        rows = [
            HtmlElement("tr", [
                HtmlElement("td", FontAwesomeIcon(
                    icon_name,
                    None,
                    HtmlAttributes({"align": "left", "style": "height: 15px;"})
                ), HtmlAttributes({"style": "text-align: left;"})),
                HtmlElement(
                    "td", tag_name, HtmlAttributes(
                        {"style": "text-align: left;"}
                    )
                ),
                HtmlElement(
                    "td", description, HtmlAttributes(
                        {"style": "text-align: left;"}
                    )
                )
            ]) for icon_name, tag_name, description in data
        ]
        content = [header, *rows]
        super().__init__(
            "table", content, HtmlAttributes({"style": "width: 100%;"})
        )

    def display(self):
        """Display tag table in IPython notebook."""
        display(HTML(str(self)))
