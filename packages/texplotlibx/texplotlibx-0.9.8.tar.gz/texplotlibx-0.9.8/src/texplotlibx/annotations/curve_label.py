from ..attribute import _tpl_attribute_function, _tpl_attribute


class _tpl_curve_label(_tpl_attribute_function):
  def __str__(self):
    v = self.get_value()
    if v == '_nolegend_':
      return _tpl_attribute.__str__(self)
    else:
      return super().__str__()
