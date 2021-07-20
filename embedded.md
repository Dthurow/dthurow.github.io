---
layout: page
categories: []
tags: []
status: publish
type: page
published: true
meta: {}
---

This page is a collection of all my embedded projects, from teardowns and reverse engineering, to documenting setting up toolchains and building custom projects.

*** 

{% assign relatedposts = site.tags["embedded"]  %}

<ul class="post-list">
      {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
      {%- for post in relatedposts -%}
      <li>
        <span class="post-meta">{{ post.date | date: date_format }}</span>
        <h3>
          <a class="post-link" href="{{ post.url | relative_url }}">
            {{ post.title | escape }}
          </a>
        </h3>
        {%- if site.show_excerpts -%}
          {{ post.excerpt }}
        {%- endif -%}
      </li>
      {%- endfor -%}
    </ul>

  