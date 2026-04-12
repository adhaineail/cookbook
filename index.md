---
layout: default
title: My Recipe Index
---

# Recipe Collection

{% assign all_pages = site.pages | sort: "path" %}

{% for page in all_pages %}
  {% if page.path contains '/' and page.title %}
    {% capture current_dir %}{{ page.path | split: "/" | first }}{% endcapture %}
    
    {% if current_dir != last_dir %}
      ## {{ current_dir | capitalize }}
      {% assign last_dir = current_dir %}
    {% endif %}

    * [{{ page.title }}]({{ page.url | relative_url }})
  {% endif %}
{% endfor %}
