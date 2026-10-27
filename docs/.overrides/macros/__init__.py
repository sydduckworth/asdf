from . import towncrier


def define_env(env):
    env.macro(towncrier.macro, "towncrier")
