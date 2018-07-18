from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_bool("like", True, "Do you like cake?")

def likes():
    if FLAGS.like:
        return "You said you like cake, yay!"
    else:
        return "You don't like cake? How sad"
