{{ name | escape | underline}}
{% set methods = filter_inherited(fullname, methods, inherited_members) %}
{% set attributes = filter_inherited(fullname, attributes, inherited_members) %}
{% set properties = filter_inherited(fullname, properties, inherited_members) %}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
    :show-inheritance:
    {% if noindex -%}
    :noindex:
    {%- endif %}

    {% if '__init__' in methods %}
        {% set caught_result = methods.remove('__init__') %}
    {% endif %}

    {% block attributes_summary %}
    {% if attributes or properties %}

    .. rubric:: Attributes Summary

    .. autosummary::
    {% for item in attributes %}
        ~{{ name }}.{{ item }}
    {%- endfor %}

    {% for item in properties %}
        ~{{ name }}.{{ item }}
    {%- endfor %}

    {% endif %}
    {% endblock %}

    {% block methods_summary %}
    {% if methods %}

    .. rubric:: Methods Summary

    .. autosummary::
    {% for item in methods %}
        ~{{ name }}.{{ item }}
    {%- endfor %}

    {% endif %}
    {% endblock %}

    {% block attributes_documentation %}
    {% if attributes or properties%}

    .. rubric:: Attributes Documentation

    {% for item in attributes %}
    .. autoattribute:: {{ item }}
    {%- endfor %}

    {% for item in properties %}
    .. autoproperty:: {{ item }}
    {%- endfor %}

    {% endif %}
    {% endblock %}

    {% block methods_documentation %}
    {% if methods %}

    .. rubric:: Methods Documentation

    {% for item in methods %}
    .. automethod:: {{ item }}
    {%- endfor %}

    {% endif %}
    {% endblock %}
