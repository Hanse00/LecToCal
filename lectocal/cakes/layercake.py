from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer("layers", 2, "Number of layers.")

def get_details():
    return "You opted for %d layer(s)." % FLAGS.layers
