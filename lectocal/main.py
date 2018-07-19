import importlib
import shlex

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_enum("cake",
                  "cakes.brownie",
                  ["cakes.brownie", "cakes.layercake"],
                  "Which cake would you like?")
flags.DEFINE_string("cake_flags", None, "List of flags for cake.")


def main(argv):
    argv.extend(shlex.split(FLAGS.cake_flags))

    print("You opted for the %s cake." % FLAGS.cake)
    module = importlib.import_module(FLAGS.cake)
    module.load_flags(argv)
    print(module.get_details())


if __name__ == "__main__":
    app.run(main)
