from absl import app
from absl import flags

import secondary

FLAGS = flags.FLAGS

flags.DEFINE_integer("cakes", 2, "How many cakes would you like?")


def main(argv):
    del argv

    print("You opted for %d cake(s)." % FLAGS.cakes)
    print(secondary.likes())


if __name__ == "__main__":
    app.run(main)
