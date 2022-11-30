from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.views import generic

from .forms import FraseForm

from .models import Idioma,Frase

class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login'


class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"


class IdiomaList(generic.ListView):
    template_name = "bases/idiomas.html"
    model = Idioma
    context_object_name="obj"



class FraseList(generic.ListView):
    template_name = "bases/frases.html"
    model = Frase
    context_object_name="obj"

    def get_queryset(self):
        qs = Frase.objects.all()
        idioma_id = self.request.GET.get("lang")
        if idioma_id:
            qs = qs.filter(idioma__id=idioma_id)
        return qs

  
class FraseView(SinPrivilegios, generic.ListView):
    permission_required = "bases:view_frases"
    model = Frase
    template_name = "bases/frases_list.html"
    context_object_name = "obj"


class FraseNew(SuccessMessageMixin,SinPrivilegios, generic.CreateView):
    model=Frase
    template_name="bases/frases_form.html"
    context_object_name = "obj"
    form_class=FraseForm
    success_url=reverse_lazy("bases:frases")
    success_message="Frase Creada Satisfactoriamente"
    permission_required="bases:add_frases"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class FraseEdit(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    model=Frase
    template_name="bases/frases_form.html"
    context_object_name = "obj"
    form_class=FraseForm
    success_url=reverse_lazy("bases:frases")
    success_message="Frase Actualizada Satisfactoriamente"
    permission_required="bases:change_frase"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class FraseDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):
    model=Frase
    template_name='bases/frases_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("bases:frases")
    success_message="Frase Eliminada"
    permission_required="bases:delete_frase"