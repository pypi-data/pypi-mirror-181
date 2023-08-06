"""
Created on 2022-08-27

@author: wf
"""
import justpy as jp




def click_demo():
    wp = jp.WebPage()
    d = jp.Button(
        text="Not clicked yet",
        a=wp,
        classes="w-48 text-xl m-2 p-1 bg-blue-500 text-white",
    )
    clickCount  = 0
    async def onDivClick(self, msg):
        """
        handle a click on the Div
        """
        nonlocal clickCount
        clickCount += 1
        d.text = f"I was clicked {clickCount} times"
    d.on("click", onDivClick)
    return wp
        
from examples.basedemo import Demo
Demo(click_demo)
