import importlib

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_enum("cake",
                  "cakes.brownie",
                  ["cakes.brownie", "cakes.layercake"],
                  "Which cake would you like?")

def main(argv):
    del argv

    print("You opted for the %s cake." % FLAGS.cake)
    module = importlib.import_module(FLAGS.cake)
    print(module.get_details())


if __name__ == "__main__":
    app.run(main)
