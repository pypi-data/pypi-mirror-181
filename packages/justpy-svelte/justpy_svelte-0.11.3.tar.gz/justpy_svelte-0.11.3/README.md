# [JustPy-Svelte](https://github.com/Monallabs-org/justpy-svelte)
---

## Introduction

Justpy-svelte is a trimmed down version of [justpy](https://justpy.io/) that replaces Vue engine with 
Svelte for the frontend. Many frontend utitiles that were build on 
Vue engine in Justpy are not supported here. Specifically, these ones:
- AGGRID 
- AGGRID_ENTERPRISE 
- BOKEH 
- DECKGL 
- HIGHCHARTS 
- KATEX 
- PLOTLY 
- QUASAR 
- QUASAR_VERSION 
- VEGA 


The surface level programming in justpy-svelte remains practically the same as Justpy. 
So all the tutorials and demos of Justpy are applicable to Justpy-Svelte. 
However, some of the core functionalities of Justpy currently are not available (see list
of examples/tutorials/tests currently passing and failing with justpy-svelte). 

Justpy-svelte is primarly designed to be driven via [ofjustpy](https://github.com/Monallabs-org/ofjustpy) - a functional programming approach to webapp development in Python. However,
it is fully functional and usable as standalone substitute for justpy. 

## Why Svelte 
Code readability, especially for non-javascript programmers, was the primary reason for porting Justpy over to Svelte. Vue on its own is powerful, has be around for longer, and has large ecosystem of libraries/tools build around it. However, I felt it was not an easy framework to pick up and comprehend, especially for non-javascript programmers. 

Comparatively, programming in  Svelte is much more straightforward and easy to comprehend 
for programmers coming from C/C++/Python/Java background. 

Its yet to be seen if Svelte offers any other advantages over Vue. 
There is good reason to hope for that. Svelte is a newer runtime and has 
very different architecture and execution paradigm, which could yield some 
advantages like being more responsive, executing faster, and better
coordination between Python runtime backend with the Javascript/Svelte frontend. 

## Notes
-  static directory by default is the directory from where the webserver is invoked


## Usage
The programming with justpy-svelte is same as [justpy](https://justpy.io/) with few difference
with respect to how starlette app  is instantiated and how routing is done.

```python
app = jp.build_app()
```
The `build_app` function takes `middlewares` and `startup_func`
as arguments using which you can pass the list of all 
[middlewares](https://www.starlette.io/middleware/)
for the app and the [startup function](https://www.starlette.io/applications/) 
to be executed at the start of the app

In order to attach a url path to a specific endpoint, i.e., perform routing
using 
p
``` python
app.add_jproute("/user/home", wp_func)
```

Rest of the usage remains the same -- checkout the examples
listed below to get a concrete sense of programming 
with justpy-svelte:


### List of examples/tests working:
- [session_test.py](/examples/tutorial/sessions/session_test.py)
- (/examples/tutorial/static/static_test.py)
- (/examples/tutorial/page_events/run_javascript_demo.py)
- (/examples/tutorial/page_events/loading_page_staggered_demo.py)
- (/examples/tutorial/custom_components/hello_test1.py)
- (/examples/tutorial/custom_components/hello_test2.py)
- (/examples/tutorial/custom_components/hello_test3.py)
- (/examples/tutorial/custom_components/hello_test4.py)
- (/examples/tutorial/custom_components/calculator_test1.py)
- (/examples/tutorial/custom_components/calculator_test2.py)
- (/examples/tutorial/custom_components/calculator_test3.py)
- (/examples/tutorial/custom_components/custom_comp_test1.py)
- (/examples/tutorial/custom_components/custom_comp_test2.py)
- (/examples/tutorial/custom_components/tab_comp_test1.py)
- (/examples/tutorial/input/check_test.py)
- (/examples/tutorial/input/color_demo.py)
- (/examples/tutorial/input/check_test.py)
- (/examples/tutorial/input/focus_test_input.py)
- (/examples/tutorial/input/input_demo1.py)
- (/examples/tutorial/input/radio_test1.py)
- (/examples/tutorial/input/radio_test2.py)
- (/examples/tutorial/working_with_html/commands_demo1.py)
- (/examples/tutorial/working_with_html/commands_demo2.py)
- (/examples/tutorial/working_with_html/html_demo.py)
- (/examples/tutorial/working_with_html/parse_demo1.py)
- (/examples/tutorial/working_with_html/parse_demo2.py)
- (/examples/tutorial/tab_group_component.py,)
- (/examples/tutorial/request_object/demo_function.py)
- (/examples/tutorial/request_object/dog_pic3.py)
- (/examples/tutorial/request_object/dog_pic2.py)
- (/examples/tutorial/request_object/dog_pic1.py)
- (/examples/tutorial/pushing_data/clock_test.py)
- (/examples/tutorial/pushing_data/count_test.py)
- (/examples/tutorial/pushing_data/message_demo.py)
- (/examples/tutorial/html_components/html_comps1.py)
- (/examples/tutorial/html_components/html_comps2.py)
- (/examples/tutorial/html_components/html_comps6.py)
- (/examples/tutorial/html_components/link_demo1.py)
- (/examples/tutorial/html_components/list_demo.py)
- (/examples/tutorial/handling_events/comp_test.py)
- (/examples/tutorial/handling_events/debounce_test.py)
- (/examples/tutorial/handling_events/event_comp_test.py)
- (/examples/tutorial/handling_events/debounce_test.py)
- (/examples/tutorial/handling_events/event_comp_test.py)
- (/examples/tutorial/handling_events/event_demo2.py)
- (/examples/tutorial/handling_events/event_demo4.py)
- (/examples/tutorial/handling_events/event_demo5.py)
- (/examples/tutorial/handling_events/event_demo6.py)
- (/examples/tutorial/handling_events/event_demo7.py)
- (/examples/tutorial/handling_events/target_test.py)

### List of test currently failing
- (/examples/multiuploads.py)
- (/examples/reference/htmlcomponent/animation_test.py)
- (/examples/reference/htmlcomponent/event_propagates.py)
- (/examples/reference/htmlcomponent/entity_test.py)
- (/examples/reference/htmlcomponent/inner_html_test.py)
- (/examples/tutorial/after_demo.py)
- (/examples/tutorial/uploading_files/)
- (/examples/tutorial/svg_components/svg_demo1.py)
- (/examples/tutorial/sessions/login_test.py)
- (/examples/tutorial/page_events/loading_page_staggered_demo.py)
- (/examples/tutorial/matplotlib/plot_test1.py)
- (/examples/tutorial/custom_components/alert_test1.py)
- (/examples/tutorial/custom_components/alert_test2.py)
- (/examples/tutorial/custom_components/custom_comp_test3.py)
- (/examples/tutorial/custom_components/custom_comp_test4.py)
- (/examples/tutorial/custom_components/custom_comp_test5.py)
- (/examples/tutorial/custom_components/grid_test.py)
- (/examples/tutorial/custom_components/table_test.py)
- (/examples/tutorial/form/form_test.py)
- (/examples/tutorial/input/input_demo2.py)
- (/examples/tutorial/input/input_demo3.py)
- (/examples/tutorial/input/input_demo4.py)
- (/examples/tutorial/input/input_demo4.py)
- (/examples/tutorial/working_with_html/inner_demo.py)
- (/examples/tutorial/model_and_data/input_demo_model1.py)
- (/examples/tutorial/model_and_data/input_demo_model2.py)
- (/examples/tutorial/html_components/link_demo2.py)
- (/examples/tutorial/html_components/show_demo.py)
- (/examples/tutorial/handling_events/event_demo3.py)
- (/examples/tutorial/handling_events/event_demo6.py)
- (/examples/tutorial/handling_events/event_demo7.py)
- (/examples/tutorial/handling_events/out_test.py)
- (/examples/tutorial/db_test.py)
- (/examples/tutorial/drag_test.py)
- (/examples/tutorial/equations/eq_test.py)
- (/examples/tutorial/ajax/reload_demo.py)

### EndNotes
- Developed By: webworks.monallabs.in 
- Docs (in readthedocs format): https://github.com/Monallabs-org/py-tailwind-utils  


