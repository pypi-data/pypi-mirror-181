from .attribute import _tpl_attribute_variable


class _tpl_cycle_list:
  def __init__(self, type="multi"):
    self.value = _tpl_attribute_variable(token="cycle %s list" % type)

  def __str__(self):
    return str(self.value)

  def repeat_style(self, times: int):
    if times is None:
      self.value.set_value(None)
    else:
      self.value.set_value("{color\\nextlist [%u of]mark list}" % times)
