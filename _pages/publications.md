---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---
<!-- TEMP WAY -->
* <strong>Look, Read and Ask: Learning to Ask Questions by Reading Text in Images</strong> <br>
  <strong>Soumya Shamarao Jahagirdar</strong>, Shankar Gangisetty, Anand Mishra <br>
  ICDAR, 2021 <br>
  [paper](https://link.springer.com/chapter/10.1007/978-3-030-86549-8_22) | [project page](https://sites.google.com/site/shankarsetty/research/textvqg) | [code](https://github.com/soumyasj/textVQG) | [video](https://www.youtube.com/watch?v=31C2wSzCxpM)

* <strong>DeepDNet: Deep Dense Network for Depth Completion Task</strong> <br>
  Girish Hegde, Tushar Pharale, <strong> Soumya Jahagirdar</strong>, Vaishakh Nargund, Ramesh Ashok Tabib, Uma Mudenagudi, Basavaraja Vandrotti, Ankit Dhiman <br>
  WiCV, CVPR, 2021 <br>
  [paper](https://openaccess.thecvf.com/content/CVPR2021W/WiCV/papers/Hegde_DeepDNet_Deep_Dense_Network_for_Depth_Completion_Task_CVPRW_2021_paper.pdf)

<!-- TEMP WAY END -->
<!-- TODO : IN FUTURE ADD PROJECS IN _projects and use the code below -->

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
