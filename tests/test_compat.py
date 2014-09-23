from mock import patch
import sys
from unittest import TestCase

import pytest

from incuna_test_utils import compat


def test_wipe_id_fields_lt_17():
    fields = ['foo', 'foo_id']
    expected_fields = ['foo']

    with patch.object(compat, 'DJANGO_LT_17', new=True):
        wiped_fields = compat.wipe_id_fields_on_django_lt_17(fields)
        assert wiped_fields == expected_fields


def test_wipe_id_fields_gte_17():
    fields = ['foo', 'foo_id']

    with patch.object(compat, 'DJANGO_LT_17', new=False):
        wiped_fields = compat.wipe_id_fields_on_django_lt_17(fields)
        assert wiped_fields == fields


@pytest.fixture(scope='module')
def testcase():
    class Python2AssertTestCase(compat.Python2AssertMixin, TestCase):
        pass

    # Python 2 doesn't allow instantiation of a TestCase without a
    # specified test method, so specify a method known to exist on
    # all TestCase instances. We don't care which method this is.
    return Python2AssertTestCase(methodName='__init__')


requires_python2 = pytest.mark.skipif(
    sys.version_info >= (3,),
    reason='Requires python 2',
)


requires_python3 = pytest.mark.skipif(
    sys.version_info < (3,),
    reason='Requires python 3',
)


@requires_python2
def test_python2_count_equal(testcase):
    assert testcase.assertCountEqual == testcase.assertItemsEqual


@requires_python3
def test_python3_count_equal(testcase):
    assert hasattr(testcase, 'assertCountEqual')


@requires_python2
def test_python2_regex(testcase):
    assert testcase.assertRegex == testcase.assertRegexpMatches


@requires_python3
def test_python3_regex(testcase):
    assert hasattr(testcase, 'assertRegex')
