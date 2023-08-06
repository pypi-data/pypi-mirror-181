#  Copyright (c) 2022. Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#  and associated documentation files (the "Software"), to deal in the Software without restriction, including without
#  limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import random
import sys
from enum import Enum, IntEnum, auto
from pathlib import Path
from typing import Any

from model_test_ui import Ui_main_model_test
from PyQt5 import QtCore
from PyQt5.Qt import QAbstractItemView, QItemSelection, QModelIndex, QStandardItem, QStandardItemModel
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QShortcut

Slot = QtCore.pyqtSlot


class UserRole(IntEnum):
    """Enumerator to define user role for the data model.

    The actual value of each role is irrelevant, it is only important that each
    element stays constant during on single execution and that their value is
    greater than QtCore.Qt.UserRole + 1.

    It is a perfect application case for an IntEnum with auto() values and
    overloaded _generate_next_value_.


    """

    # noinspection PyProtectedMember
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> int:
        """
        Generate the next value.

        This function is called every time a new element with auto() is added.
        The user role must be at least QtCore.Qt.UserRole + 1.

        Parameters
        ----------
        name : string
            The name of the enum element.
        start : int
            The value of the first enumerator. It is always 1.
        count : int
            The number of enumerator values so far.
        last_values : iterable
            A list of all already used values.

        Returns
        -------
        int
            The next value starting from QtCore.Qt.UserRole+1

        """
        return IntEnum._generate_next_value_(name, QtCore.Qt.UserRole + 1, count, last_values)

    ITEM_TYPE = auto()
    DESCRIPTION = auto()
    EXTRA = auto()
    IMAGE = auto()
    PIC_ID = auto()
    CAPTION = auto()
    SAMPLE_FULL_NAME = auto()
    SAMPLE_LAST_NAME = auto()
    ATTACHMENT_PATH = auto()
    ATTACHMENT_FILE = auto()
    VIDEO_KEY = auto()
    VIDEO_PATH = auto()
    VIDEO_URL = auto()


class ElementType(Enum):
    """Enumerator to define the various type of items."""

    TEXT = 'Text'
    SECTION = 'Section'
    SAMPLE = 'Sample'
    NAVIGATION_PIC = 'NavPic'
    MICROSCOPE_PIC = 'MicroPic'
    ATTACHMENT_FILE = 'AttachmentFile'
    YAML_FILE = 'YAMLFile'
    VIDEO_FILE = 'VIDEOFile'


class TextItem(QStandardItem):
    """Text item derived from QStandardItem."""

    def __init__(self, txt=''):
        """
        Construct a new TextItem.

        The item_type role is set to Text.

        Parameters
        ----------
        txt : str, optional
            This is the text used as a display role. The default is ''.

        Returns
        -------
        None.
        """
        super().__init__()
        self.setText(txt)
        self.setData(ElementType.TEXT, UserRole.ITEM_TYPE)


class SectionItem(TextItem):
    """
    Section item derived from TextItem.

    This item is used to store section information.

    """

    def __init__(self, txt=''):
        """
        Construct a new SectionItem.

        The item_type role is set to Section.

        Parameters
        ----------
        txt : str, optional
            This is the text used as a display role. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData(ElementType.SECTION, UserRole.ITEM_TYPE)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.text()
        if key in yaml_dict.keys():
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class AttachmentItem(QStandardItem):
    """
    Attachment item derived from QStandardItem.

    This item is used to store attachments.
    The display name is the attachment filename.

    The attachment key is stored in the data with attachment_path.
    The attachment filename is stored in the with attachment_file

    """

    def __init__(self, attachment_path):
        super().__init__()
        attachment_filename = Path(attachment_path).name
        self.setText(attachment_filename)
        self.setData(ElementType.ATTACHMENT_FILE, UserRole.ITEM_TYPE)
        self.setData(attachment_path, UserRole.ATTACHMENT_PATH)
        self.setData(attachment_filename, UserRole.ATTACHMENT_FILE)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve custom information for this element from a dictionary

        Parameters
        ----------
        yaml_dict: dict
            The dictionary with the customization information.

        """
        key = self.data(UserRole.ATTACHMENT_PATH)
        if key in yaml_dict.keys():
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class SampleItem(QStandardItem):
    """
    Sample item derived from QStandardItem.

    This item is used to store samples.

    The Display name is the sample_last_name.

    The sample_full_name is stored in the data with the sample_full_name_role.
    The sample_last_name is stored in the data with the sample_last_name_role.

    """

    def __init__(self, sample_full_name):
        """
        Generate a new Sample Item.

        Remeber that this object needs the **full name**.

        The display text (what will appear on the Protocol Editor) is the last
        name, but the constructur needs the full name.

        Parameters
        ----------
        sample_full_name : str
            Full name (complete hierarchy) of the sample.

        Returns
        -------
        None.

        """
        super().__init__()
        sample_last_name = sample_full_name.split('/')[-1]
        self.setText(sample_last_name)
        self.setData(ElementType.SAMPLE, UserRole.ITEM_TYPE)
        self.setData(sample_full_name, UserRole.SAMPLE_FULL_NAME)
        self.setData(sample_last_name, UserRole.SAMPLE_LAST_NAME)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : Dictionary
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.data(UserRole.SAMPLE_FULL_NAME)
        if key in yaml_dict.keys():
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class NavPicItem(TextItem):
    """
    Navigation Picture Item.

    This type is used to store navigation images.
    """

    def __init__(self, txt='', img_link=''):
        """
        Constructur an instance of NaPicItem.

        The type of this item is set to NavPic.

        Parameters
        ----------
        txt : str, optional
            The name of the picture used as display_role. The default is ''.
        img_link : str, optional
            The URL where the thumbnail of the image. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData(ElementType.NAVIGATION_PIC, UserRole.ITEM_TYPE)
        self.setData(img_link, UserRole.IMAGE)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.text()
        if key in yaml_dict.keys():
            if 'Caption' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Caption'], UserRole.CAPTION)
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class MicroPicItem(TextItem):
    """
    Microscope Picture Item.

    This type is used to store microscope pictures.
    """

    def __init__(self, txt='', img_id=0, img_link=''):
        """
        Constructor an instance of MicroPicItem.

        The type of this item is set to MicroPic.

        Parameters
        ----------
        img_id : int, optional
            The identification number of the microscope image. The default is 0.

        img_link : str, optional
            The URL where the thumbnail of the image. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData(ElementType.MICROSCOPE_PIC, UserRole.ITEM_TYPE)
        self.setData(img_id, UserRole.PIC_ID)
        self.setData(img_link, UserRole.IMAGE)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        pic_id = int(self.data(UserRole.PIC_ID))
        if pic_id in yaml_dict.keys():
            pass
        elif int(pic_id) in yaml_dict.keys():
            pic_id = int(pic_id)
        else:
            return
        if 'Caption' in yaml_dict[pic_id].keys():
            self.setData(yaml_dict[pic_id]['Caption'], UserRole.CAPTION)
        if 'Description' in yaml_dict[pic_id].keys():
            self.setData(yaml_dict[pic_id]['Description'],
                         UserRole.DESCRIPTION)
        if 'Extra' in yaml_dict[pic_id].keys():
            self.setData(yaml_dict[pic_id]['Extra'], UserRole.EXTRA)


class VideoItem(TextItem):
    """Video item."""

    def __init__(self, txt: str = '', key: str = '', url: str = '', path: str | Path = ''):
        """Build an instance of VideoItem"""
        super().__init__(txt=txt)
        self.setData(ElementType.VIDEO_FILE, UserRole.ITEM_TYPE)
        self.setData(key, UserRole.VIDEO_KEY)
        self.setData(path, UserRole.VIDEO_PATH)
        self.setData(url, UserRole.VIDEO_URL)

    def get_data_from_yaml(self, yaml_dict: dict) -> None:
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yaml_dict : dict
            YAML Dictionary where the information of the item are stored.

        Returns
        -------
        None.
        """
        key = self.data(UserRole.VIDEO_KEY)
        if key in yaml_dict.keys():
            if 'Caption' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Caption'], UserRole.CAPTION)
            if 'Description' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Description'],
                             UserRole.DESCRIPTION)
            if 'Extra' in yaml_dict[key].keys():
                self.setData(yaml_dict[key]['Extra'], UserRole.EXTRA)


class MainWindow_ModelTest(QMainWindow, Ui_main_model_test):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.pic_id = 0
        self.sample_id = 4

        self.tree_model = QStandardItemModel()
        self.root_node = self.tree_model.invisibleRootItem()
        self.generate_model()
        self.treeView.setModel(self.tree_model)
        self.treeView.collapseAll()
        self.listView.setModel(self.tree_model)

        self.listView.setSelectionModel(self.treeView.selectionModel())

        items = self.tree_model.findItems('sample1', QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
        self.listView.setRootIndex(items[0].index())

        self.tree_model.rowsInserted.connect(self.react_to_new_rows)
        self.treeView.selectionModel().selectionChanged.connect(self.selection_change)

        self.timer = QTimer()
        self.timer.timeout.connect(self.add_image)
        self.timer.start(5000)

    @Slot(QItemSelection, QItemSelection)
    def selection_change(self, new_item: QItemSelection, old_item: QItemSelection):
        indexes = new_item.indexes()
        if len(indexes) != 1:
            print('error')
        else:
            item = self.tree_model.itemFromIndex(indexes[0])
            self.select_label.setText(f'Selected element is {item.data(QtCore.Qt.DisplayRole)}')
            if item.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                self.sampleSelector.setCurrentText(item.data(QtCore.Qt.DisplayRole))
            if item.data(UserRole.ITEM_TYPE) == ElementType.MICROSCOPE_PIC:
                self.sampleSelector.setCurrentText(item.parent().data(QtCore.Qt.DisplayRole))

    @Slot(QModelIndex, int, int)
    def react_to_new_rows(self, parent: QModelIndex, start, stop):
        for row in range(start, stop + 1):
            new_row = self.tree_model.index(row, 0, parent)
            if new_row.data(UserRole.ITEM_TYPE) == ElementType.SAMPLE:
                self.sampleSelector.addItem(new_row.data(QtCore.Qt.DisplayRole))


    @Slot(str)
    def changeListRoot(self, root_name):
        items = self.tree_model.findItems(root_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
        if len(items) != 1:
            print(f'error-change list {root_name=} and {len(items)=}')
        else:
            self.listView.setRootIndex(items[0].index())

    def add_sample(self):
        items = self.tree_model.findItems('Samples')
        if len(items) != 1:
            print('error')
        else:
            sample_item = SampleItem(f'sample{self.sample_id}')
            items[0].appendRow(sample_item)
            self.sample_id += 1

    def generate_model(self):
        navpics = [('navipic1', f'{Path.cwd()}/navipic1.png'),
                   ('navipic2', f'{Path.cwd()}/navipic1.png')]
        samples = ['sample1', 'sample2', 'sample3']

        introduction_section = SectionItem('Introduction')
        self.root_node.appendRow(introduction_section)

        navcam_section = SectionItem('Navigation images')
        for name, path in navpics:
            navpic_item = NavPicItem(name, path)
            navcam_section.appendRow(navpic_item)

        self.root_node.appendRow(navcam_section)

        sample_section = SectionItem('Samples')
        for sample in samples:
            sample_item = SampleItem(sample)
            for picture in range(5):
                pic_item = MicroPicItem(f'micro_pic_{self.pic_id}', self.pic_id)
                sample_item.appendRow(pic_item)
                self.pic_id += 1
            sample_section.appendRow(sample_item)
            self.sampleSelector.addItem(sample)

        self.root_node.appendRow(sample_section)

        conclusion_section = SectionItem('Conclusion')
        self.root_node.appendRow(conclusion_section)

    def add_image(self):
        sample = f'sample{random.choice(range(1,self.sample_id))}'
        items = self.tree_model.findItems(sample, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
        if len(items) > 1:
            print('error')
        else:
            pic_item = MicroPicItem(f'micro_pic_{self.pic_id}', self.pic_id)
            items[0].appendRow(pic_item)
            self.treeView.scrollTo(self.tree_model.indexFromItem(pic_item))
            self.pic_id += 1


def main():
    app = QApplication(sys.argv)
    win = MainWindow_ModelTest(app)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
