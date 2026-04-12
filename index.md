---
layout: default
title: My Recipe Index
---

# 📖 Recipe Collection

{% assign recipes_by_folder = site.pages | group_by_exp: "item", "item.path | split: '/' | first" %}

{% for folder in recipes_by_folder %}
  {% unless folder.name contains '.md' or folder.name == "assets" %}
    
    ## {{ folder.name | replace: "-", " " | replace: "_", " " | capitalize }}
    
    <ul>
      {% for recipe in folder.items %}
        {% if recipe.title %}
          <li>
            <a href="{{ site.baseurl }}{{ recipe.url }}">{{ recipe.title }}</a>
          </li>
        {% endif %}
      {% endfor %}
    </ul>

  {% endunless %}
{% endfor %}
