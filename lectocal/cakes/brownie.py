from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string("filling", "nuts", "The brownie filling.")

def get_details():
    return "Your brownies will contain %s." % FLAGS.filling


def load_flags(argv):
    print(argv)
    app.parse_flags_with_usage(argv)
