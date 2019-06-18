from cliglue.builder import *
from tests.asserts import MockIO


def test_args_container_by_attr():
    def print_args_dict(args):
        print(' '.join([
            args.param, args.p,
            str(args.p2),
            args.multi_ple_words,
            args.nnn,
        ]))

    with MockIO('--param', 'pval', '--multi-ple-words', 'words', '--p2', '--named-param=mmm') as mockio:
        CliBuilder(run=print_args_dict).has(
            parameter('param', '-p'),
            flag('p2'),
            parameter('multi-ple-words'),
            parameter('named-param', name='nnn'),
        ).run()
        assert mockio.stripped_output() == 'pval pval True words mmm'


def test_args_container_by_dict_name():
    def print_args_dict(args):
        print(' '.join([
            args['param'], args['--param'], args['p'], args['-p'],
            str(args['p2']), str(args['--p2']),
            args['multi-ple-words'], args['multi_ple_words'],
            args['nnn'],
        ]))

    with MockIO('--param', 'pval', '--multi-ple-words', 'words', '--p2', '--named-param=mmm') as mockio:
        CliBuilder(run=print_args_dict).has(
            parameter('param', '-p'),
            flag('p2'),
            parameter('multi-ple-words'),
            parameter('named-param', name='nnn'),
        ).run()
        assert mockio.stripped_output() == 'pval pval pval pval True True words words mmm'
