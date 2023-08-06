from .attribute import _tpl_attribute_variable
from .util import _isfloat


class _tpl_limits:
  def __init__(self):
    self.xmin = _tpl_attribute_variable(token='xmin')
    self.ymin = _tpl_attribute_variable(token='ymin')
    self.xmax = _tpl_attribute_variable(token='xmax')
    self.ymax = _tpl_attribute_variable(token='ymax')

  def __str__(self):
    return f"""{self.xmin}
  {self.xmax}
  {self.ymin}
  {self.ymax}"""

  def set_xlim(self, left: float, right: float):
    something_done = False
    if left is not None and _isfloat(left):
      self.xmin.set_value(left)
      something_done = True
    if right is not None and _isfloat(right):
      self.xmax.set_value(right)
      something_done = True
    if isinstance(left, (tuple, list)) and right is None and len(left) == 2:
      self.xmin.set_value(left[0])
      self.xmax.set_value(left[1])
      something_done = True
    if not something_done:
      print("texplotlib: Setting xlim: Cannot interpret arguments")

  def _set_ylim(self, left: float, right: float):
    something_done = False
    if left is not None and _isfloat(left):
      self.ymin.set_value(left)
      something_done = True
    if right is not None and _isfloat(right):
      self.ymax.set_value(right)
      something_done = True
    if isinstance(left, (tuple, list)) and right is None and len(left) == 2:
      self.ymin.set_value(left[0])
      self.ymax.set_value(left[1])
      something_done = True
    if not something_done:
      print("texplotlib: Setting ylim: Cannot interpret arguments")
