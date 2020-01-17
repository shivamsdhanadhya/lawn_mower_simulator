"""simulation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import simulations.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^simulation/', simulations.views.simulation),
    url(r'^getInfo/', simulations.views.getInfo),
    url(r'^nextMove/', simulations.views.nextMove),
    url(r'^restart/', simulations.views.restart),
    url(r'^fastForward/', simulations.views.fastForward),
    url(r'^stop/', simulations.views.stop),
    url(r'^uploadFile/', simulations.views.uploadFile),
    url(r'^/', simulations.views.redirectToSimulation),
]
