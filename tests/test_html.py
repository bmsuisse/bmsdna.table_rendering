import polars as pl

from bmsdna.table_rendering import TableRenderer, ColumnConfig


def test_render_html_tr_styles_callable():
    fake_data = pl.DataFrame(
        data=[
            {"a": 1},
            {"a": 2},
        ]
    )
    rend = TableRenderer.from_df(fake_data)

    html = rend.render_html(
        fake_data,
        tr_styles=lambda row: {"background-color": "red" if row["a"] == 1 else "blue"},
    )

    assert "background-color: red" in html
    assert "background-color: blue" in html
    red_dict = {"background-color": "red"}
    blue_dict = {"background-color": "blue"}
    html2 = rend.render_html(
        fake_data,
        tr_styles=lambda row: red_dict if row["a"] == 1 else blue_dict,
    )
    assert "background-color: red" in html2
    assert "background-color: blue" in html2

    html3 = rend.render_html(
        fake_data,
        tr_styles="background-color: green",
    )
    assert "background-color: green" in html3

    green_dict = {"background-color": "green"}
    html4 = rend.render_html(
        fake_data,
        tr_styles=green_dict,
    )
    assert "background-color: green" in html4


def test_render_html_links():
    fake_data = pl.DataFrame(
        data=[
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
    )
    rend = TableRenderer(
        [
            ColumnConfig(
                field="name",
                link=lambda value, _: f"https://example.com/users/{value.lower()}",
                header_key="tester",
            )
        ],
        translator=lambda key, _: {"tester": "Name"}[key],
    )

    html = rend.render_html(fake_data)

    assert '<a href="https://example.com/users/alice">Alice</a>' in html
    assert '<a href="https://example.com/users/bob">Bob</a>' in html
