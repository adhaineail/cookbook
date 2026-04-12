---
layout: default
title: Recipe Index
---
{% assign recipes_by_folder = site.pages | group_by_exp: "item", "item.path | split: '/' | first" %}

{% for folder in recipes_by_folder %}
  {% unless folder.name contains '.md' %}
    ## {{ folder.name | capitalize }}
    <ul>
      {% for recipe in folder.items %}
        <li><a href="{{ recipe.url | relative_url }}">{{ recipe.title | default: recipe.name }}</a></li>
      {% endfor %}
    </ul>
  {% endunless %}
{% endfor %}