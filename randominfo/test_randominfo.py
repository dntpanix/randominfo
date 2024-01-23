import unittest

from __init__ import *


class PersonClassTest(unittest.TestCase):
    """
    Test of getting attributes for class Person and
    correct work for personal methods of class.
    """
    def setUp(self):
        self.person_01 = Person()
        self.person_02 = Person(gender='male')

    def test_p01(self):
        """ Test of correct display gender """
        expected_res = 'male'
        actual_res = self.person_02.gender
        self.assertEqual(expected_res, actual_res, msg="Genders are not match!")

    def test_p02(self):
        """ Test of correct display full name """
        expected_res = self.person_01.first_name + " " + self.person_01.last_name
        actual_res = self.person_01.full_name
        self.assertEqual(expected_res, actual_res, msg="Full name isn't correct")

    def test_p03(self):
        """ Test of correct setting attribute for Person class instance """
        self.person_02.set_attr('newattr', 'test attribute')
        expected_res = 'test attribute'
        actual_res = self.person_02.get_attr('newattr')
        self.assertEqual(expected_res, actual_res, msg="New attribute didn't setting")

    def test_n01(self):
        """ Test of setting incorrect attribute for Person class instance"""
        expected_res = ValueError
        with self.assertRaises(ValueError):
            actual_result = self.person_02.set_attr('1newattr')

    def test_n02(self):
        """ Test of setting incorrect attribute for Person class instance"""
        expected_res = ValueError
        with self.assertRaises(ValueError):
            actual_result = self.person_02.set_attr('new_attr')

    def tearDown(self):
        pass


class GettingIdTest(unittest.TestCase):
    """
    Test of correct get_id() function work
    """
    def test_p04(self):
        """Test of correct length"""
        expected_res = 6
        actual_res = len(get_id(6))
        self.assertEqual(expected_res, actual_res, msg="Lenght isn't match")

    def test_p05(self):
        """Test of correct seq_number """
        expected_res = '11'
        actual_res = get_id(seq_number=10)
        self.assertEqual(expected_res, actual_res, msg="Seq number doesn't work")

    def test_p06(self):
        """Test of correct seq_number with step """
        expected_res = '15'
        actual_res = get_id(seq_number=10, step=5)
        self.assertEqual(expected_res, actual_res, msg="Seq number or step doesn't work")

    def test_p07(self):
        """Test of correct seq_number with step """
        expected_res = '15'
        actual_res = get_id(seq_number=10, step=5)
        self.assertEqual(expected_res, actual_res, msg="Seq number or step doesn't work")

    def test_p08(self):
        """Test of correct assign prefix and postfix """
        actual_res = get_id(prefix='id_', postfix='_FUNC')
        expected_prefix = actual_res.startswith('id_')
        expected_postfix = actual_res.endswith('_FUNC')

        self.assertTrue(expected_prefix, msg="Prefix doesn't match!")
        self.assertTrue(expected_postfix, msg="Postfix doesn't match!")


class GettingAddressTest(unittest.TestCase):
    """
    Test of correct get_address() function work
    """
    def test_p09(self):
        """Test of correct keys in result dict"""
        expected_keys = {'street address', 'landmark', 'area', 'city', 'state', 'pincode'}
        actual_res = get_address()
        self.assertSetEqual(expected_keys, set(actual_res.keys()), msg="Keys do not match!")

    def test_p10(self):
        """Test of valid rows"""
        actual_res = get_address()
        expected_res = actual_res.values() is not None
        self.assertTrue(expected_res, msg="Validation of rows is fail")