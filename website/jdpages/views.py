from django.shortcuts import render


def get_elements_with_items(elements):
    elements_new = []
    for element in elements:
        if element.content_type.model_class() == BlogCategory:
            elements_new.append(BlogCategoryElement.get_original_element(element))
    return elements_new
