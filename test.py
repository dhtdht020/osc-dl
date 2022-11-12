import pytest
from PySide6 import QtCore

import xosc_dl


@pytest.fixture
def app(qtbot):
    oscdl_app = xosc_dl.MainWindow(test_mode=True)
    qtbot.addWidget(oscdl_app)

    return oscdl_app


def test_download(app, qtbot):
    qtbot.mouseClick(app.ui.ViewMetadataBtn, QtCore.Qt.LeftButton)
    while app.ui.progressBar.value() < 100:
        pass
    assert "completed successfully" in app.ui.statusBar.currentMessage()


def test_search(app, qtbot):
    qtbot.mouseClick(app.ui.ViewMetadataBtn, QtCore.Qt.LeftButton)
    qtbot.keyClicks(app.ui.SearchBar, 'Danbo')
    assert "1" in app.ui.AppsAmountLabel.text()


def test_app_meta(app):
    # get index of Danbo
    for i in range(app.ui.listAppsWidget.count()):
        if "Danbo" in app.ui.listAppsWidget.item(i).text():
            app.ui.listAppsWidget.setCurrentRow(i)

    # Assert selection changed
    assert "Danbo" in app.ui.listAppsWidget.currentItem().text()

    # Assert metadata applied
    assert "Danbo" == app.ui.developer.text()


def test_app_long_description(app):
    # get index of Danbo
    for i in range(app.ui.listAppsWidget.count()):
        if "Danbo" in app.ui.listAppsWidget.item(i).text():
            app.ui.listAppsWidget.setCurrentRow(i)

    # set to description tab
    app.ui.tabMetadata.setCurrentIndex(1)

    # assert description
    assert "Danbo" == app.ui.longDescriptionBrowser.toPlainText()
