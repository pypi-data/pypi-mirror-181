from ..attribute import _tpl_attribute_variable


class _tpl_mark:
  def __init__(self, mark, fill, scale):
    self.mark: _tpl_attribute_variable = _tpl_attribute_variable(token='mark', value=mark)
    self.fill: _tpl_attribute_variable = _tpl_attribute_variable(token='fill', value=fill)
    self.scale: _tpl_attribute_variable = _tpl_attribute_variable(token='scale', value=scale)

  def __options(self):
    return f"""mark options={{
    {self.scale}
    {self.fill}
  }}"""

  def __options_active(self):
    if self.fill.get_value() is not None:
      return True
    if self.scale.get_value() is not None:
      return True
    return False

  def __str__(self):
    return f"""{self.mark}
  {self.__options() if self.__options_active() else '% mark options'}"""
