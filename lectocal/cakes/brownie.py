from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string("filling", "nuts", "The brownie filling.")

def get_details():
    return "Your brownies will contain %s" % FLAGS.filling
