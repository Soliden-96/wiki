from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django import forms
from django.urls import reverse
import random
import markdown2

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'placeholder':'Title','class':'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'placeholder':'Content','class':'form-control'}))


def index(request):

    if request.method == "POST":
        title = request.POST.get("q")

        if title not in util.list_entries():
            newList = []
            for name in util.list_entries():
                if title.lower() in name.lower():
                    newList.append(name)
            
            if len(newList) == 0:
                return HttpResponseNotFound(render(request, "encyclopedia/error.html", {
                    "error_message": "No similar pages found", "status":"404"
                }))

            return render(request,"encyclopedia/didYouMean.html",{
                "list":newList
            })


        markdownContent = util.get_entry(title)
        content = markdown2.markdown(markdownContent)
        return render(request,"encyclopedia/content.html",{
            "title":title, "content":content
        })
        


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request,title):

    if title not in util.list_entries():
        return HttpResponseNotFound(render(request, "encyclopedia/error.html", {
                    "error_message": "This page doesn't exist", "status":"404"
                }))

   
    markdownContent = util.get_entry(title)
    content = markdown2.markdown(markdownContent)

   

    return render(request, "encyclopedia/content.html", {
        "title":title, "content":content
    })

def newPage(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return HttpResponseBadRequest(render(request, "encyclopedia/error.html", {
                    "error_message": "A page with this title already exists, you can edit that page", "status":"400"
                }))
            util.save_entry(title,content)
            return redirect(reverse("content",args=[title]))


    return render(request,"encyclopedia/newPage.html",{
        "form":NewPageForm()
    })

def edit(request,title):

    content = util.get_entry(title)
    form = NewPageForm(request.POST)
    
    if request.method == "POST":
        new_title = request.POST.get("title")
        new_content = request.POST.get("content")
        util.save_entry(title,new_content)
        return redirect(reverse("content",args=[title]))



    return render(request,"encyclopedia/edit.html",{
        "title":title, "content":content, "form":form
    })

def randomPage(request):
    list = util.list_entries()
    num = random.randint(0,len(list)-1)
    title = list[num]
    return redirect(reverse("content",args=[title]))


