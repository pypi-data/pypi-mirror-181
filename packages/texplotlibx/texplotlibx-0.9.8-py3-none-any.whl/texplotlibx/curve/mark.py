from ..attribute import _tpl_attribute_variable


class _tpl_mark:
  def __init__(self, value):
    self.mark: _tpl_attribute_variable = _tpl_attribute_variable(token='mark', value=value)

  def __str__(self):
    return str(self.mark)
