from cliglue.builder import *
from tests.asserts import MockIO


def test_empty_builder():
    with MockIO() as mockio:
        CliBuilder()
        mockio.assert_output('')
    with MockIO():
        CliBuilder(with_defaults=False).run()