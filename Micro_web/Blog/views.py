#from django.shortcuts import render
#

#
#class profile(CreateView):
#    model =  Profile
#    fields = ['bio', 'photo']
#    template_name = 'Blog/myProfile.html'
#    success_url = '/newsfeed/'
#    def form_valid(self, form):
#        form.instance.user = self.request.user
#        return super().form_valid(form)
