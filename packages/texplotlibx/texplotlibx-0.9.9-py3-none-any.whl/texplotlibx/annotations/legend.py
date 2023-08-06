from ..attribute import _tpl_attribute_variable


class _tpl_legend:
  def __init__(self):
    self.pos = _tpl_attribute_variable(token="legend pos")

  @staticmethod
  def __expand(value: str) -> str:
    if value == 'n':
      return 'north'
    if value == 's':
      return 'south'
    if value == 'e':
      return 'east'
    if value == 'w':
      return 'west'
    if value == 'o':
      return 'outer'

  def _set_position(self, value: str):
    if len(value) <= 3:
      expanded = [self.__class__.__expand(s) for s in value]
      value = ' '.join(expanded)
    self.pos.set_value(value)
