#author:Haoqiu Wu Time 19.2.27
from .forms import SearchForm
from haystack.views import SearchView

# see how to do chinese search engine, https://www.cnblogs.com/xuaijun/p/8027606.html
# intro to classed based view,https://docs.djangoproject.com/en/2.0/topics/class-based-views/intro/
class ArticleSearchView(SearchView):
    def extra_context(self):
        context_variable=super(ArticleSearchView,self).extra_context()
        context_variable['form']=SearchForm()
        context_variable['new_feature']="new feature"
        return context_variable

