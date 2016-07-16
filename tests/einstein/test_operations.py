import base64
from unittest import TestCase

import ims.common.constants as constants
import ims.einstein.ceph as ceph
from ims.database import *
from ims.einstein.operations import BMI

_cfg = config.get()

CORRECT_HAAS_USERNAME = "haasadmin"
CORRECT_HAAS_PASSWORD = "admin1234"
INCORRECT_HAAS_PASSWORD = "admin123##"

NODE_NAME = "cisco-27"
CHANNEL = "vlan/native"
NIC = "enp130s0f0"

PROJECT = "bmi_infra"
NETWORK = "bmi-provision"

EXIST_IMG_NAME = "bmi_ci.img"
NOT_EXIST_IMG_NAME = "i12"
NOT_EXIST_SNAP_NAME = "hello"

credentials = (
    base64.b64encode(CORRECT_HAAS_USERNAME + ":" + CORRECT_HAAS_PASSWORD),
    PROJECT,)


class TestProvision(TestCase):
    def setUp(self):
        self.db = Database()
        self.db.project.insert(PROJECT, NETWORK)
        import_test(EXIST_IMG_NAME)

        self.good_bmi = BMI(credentials)

    def test_run(self):
        response = self.good_bmi.provision(NODE_NAME, EXIST_IMG_NAME, NETWORK,
                                           CHANNEL, NIC)
        self.assertEqual(response[constants.STATUS_CODE_KEY], 200)

    def tearDown(self):
        self.good_bmi.deprovision(NODE_NAME, NETWORK, NIC)
        self.good_bmi.remove_image(EXIST_IMG_NAME)
        self.db.project.delete_with_name(PROJECT)
        self.db.close()
        self.good_bmi.shutdown()


class TestDeprovision(TestCase):
    def setUp(self):
        self.db = Database()
        self.db.project.insert(PROJECT, NETWORK)
        import_test(EXIST_IMG_NAME)

        self.good_bmi = BMI(credentials)
        self.good_bmi.provision(NODE_NAME, EXIST_IMG_NAME, NETWORK,
                                CHANNEL, NIC)

    def test_run(self):
        response = self.good_bmi.deprovision(NODE_NAME, NETWORK, NIC)
        self.assertEqual(response[constants.STATUS_CODE_KEY], 200)

    def tearDown(self):
        self.good_bmi.remove_image(EXIST_IMG_NAME)
        self.db.project.delete_with_name(PROJECT)
        self.db.close()
        self.good_bmi.shutdown()


class TestCreateSnapshot(TestCase):
    def setUp(self):
        pass

    def test_run(self):
        pass

    def tearDown(self):
        pass


class TestListSnapshots(TestCase):
    def setUp(self):
        pass

    def test_run(self):
        pass

    def tearDown(self):
        pass


class TestRemoveSnapshot(TestCase):
    def setUp(self):
        pass

    def test_run(self):
        pass

    def tearDown(self):
        pass


class TestListImages(TestCase):
    def setUp(self):
        pass

    def test_run(self):
        pass

    def tearDown(self):
        pass


class TestRemoveImage(TestCase):
    def setUp(self):
        pass

    def test_run(self):
        pass

    def tearDown(self):
        pass


def import_test(img):
    with ceph.RBD(_cfg.fs[constants.CEPH_CONFIG_SECTION_NAME]) as fs:
        with Database() as db:
            pid = db.project.fetch_id_with_name(project)
            ceph_img_name = str(img)

            fs.snap_image(ceph_img_name, constants.DEFAULT_SNAPSHOT_NAME)
            fs.snap_protect(ceph_img_name, constants.DEFAULT_SNAPSHOT_NAME)
            db.image.insert(ceph_img_name, pid)
            snap_ceph_name = __get__ceph_image_name(ceph_img_name, project)
            fs.clone(ceph_img_name, constants.DEFAULT_SNAPSHOT_NAME,
                     snap_ceph_name)
            fs.flatten(snap_ceph_name)
            fs.snap_image(snap_ceph_name, constants.DEFAULT_SNAPSHOT_NAME)
            fs.snap_protect(snap_ceph_name,
                            constants.DEFAULT_SNAPSHOT_NAME)
            fs.snap_unprotect(ceph_img_name,
                              constants.DEFAULT_SNAPSHOT_NAME)
            fs.remove_snapshot(ceph_img_name,
                               constants.DEFAULT_SNAPSHOT_NAME)


def __get__ceph_image_name(name, project):
    with Database() as db:
        img_id = db.image.fetch_id_with_name_from_project(name, project)
        if img_id is None:
            logger.info("Raising Image Not Found Exception for %s", name)
            raise db_exceptions.ImageNotFoundException(name)

        return str(_cfg.uid) + "img" + str(img_id)