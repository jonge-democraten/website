from django import template

register = template.Library()

@register.filter
def divisible(value, divisor):
  return value % divisor == 0

