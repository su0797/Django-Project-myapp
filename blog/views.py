from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
# generic은 미리 생성된 기능이 많다
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm, HashTagForm
from django.urls import reverse_lazy, reverse

# Create your views here.
# def index(request):
#     if request.method == 'GET':
#         return HttpResponse('Index page GET')
#     # 나머지 요청 
#     # 에러, 예외처리
#     return HttpResponse('No!!')


### Post
class Index(View):
    def get(self, request):
        # return HttpResponse('Index page GET class')
        
        # 데이터베이스에 접근해서 값을 가져와야 합니다.
        # 게시판에 글들을 보여줘야하기 때문에 데이터베이스에서 "값 조회"
        # MyModel.objects.all()
        post_objs = Post.objects.all()
        # context = 데이터베이스에서 가져온 값
        context = {
            "posts": post_objs
        }
        # print(post_objs) QuerySet<[post 1, 2, 3, 4, 5]>
        return render(request, 'blog/post_list.html', context)

'''
class Index(LoginRequiredMixin, View):
    def get(self, request):
        # Post - User 연결 (Foreignkey)
        # User를 이용해서 Post를 가지고 온다.
        posts = Post.objects.filter(writer=request.user)
        context = {
            "posts" : posts
        }
        return render(request, 'blog/post_list.html', context)
'''

# write
# post - form
# 글 작성 화면
# def write(request):
#     if request.method == 'POST':
#         # form 확인
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save()
#             return redirect('blog:list')

#     # else: # 위에서 if가 끝나는 경우 else를 생략할 수 있음
#     form = PostForm()
#     return render(request, 'blog/write.html', {'form' : form})


# Django 자체의 클래스 뷰 기능도 강력, 편리
# model, template_name, context_object_name,
# paginate_by, form_class, form_valid(), get_queryset()
# django.views.generic -> ListView
# class List(ListView):
#     model = Post # 모델
#     template_name = 'blog/post_list.html' # 탬플릿
#     context_object_name = 'posts' # 변수 값의 이름


# class Write(CreateView):
#     model = Post # 모델
#     form_class = PostForm # 폼
#     success_url = reverse_lazy('blog:list') # 성공시 보내줄 url

class Write(LoginRequiredMixin, View):
    # Mixin: LoginRequiredMixin 별도의 클래스로 정의됨
    def get(self, request):
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # commit=False 변수 할당만 우선 하고 이후에 수정가능
            post.writer = request.user
            post.save() # 값이 할당되면 save
            return redirect('blog:list') # response -> HttpResponse 객체
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form
        }
        return render(request, 'blog/post_form.html')


# class Detail(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#     context_object_name = 'post'


class Update(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']
    # success_url = reverse_lazy('blog:list')

    # initial 기능 사용 -> form에 값을 미리 넣어주기 위해서 
    def get_initial(self):
        initial = super().get_initial()  # UpdateView(generic view)에서 제공하는 initial(딕셔너리)
        post = self.get_object() # generic으로 만들면 상속 받는 것 / pk 기반으로 객체를 가져온다
        initial['title'] = post.title
        initial['content'] = post.content
        return initial

    def get_success_url(self): # get_absolute_url 이것도 자주 씀
        post = self.get_object() # pk 기반으로 현재 객체 가져오기
        return reverse('blog:detail', kwargs={'pk' : post.pk})
    
    
# class Delete(DeleteView):
#     model = Post
#     success_url = reverse_lazy('blog:list')


class Delete(View):
    # 삭제페이지는 따로 보여줄 필요가 없기 때문에 post만 사용
    def post(self, request, pk): # post_id
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('blog:list')
    
    # 클래스 자체에 아예 접근하지 못하게 -> LoginRequiredMixin
    # Login만 되었을 때만 삭제 버튼이 보이게 



class DetailView(View):
    def get(self, request, pk): # post_id : 데이터베이스 post_id 테이블 이름 사용하고 싶어서  씀
        # list -> object 상세 페이지 -> 상세 페이지 하나의 내용
        # pk 값을 왔다 갔다 -> pk는 하나의 인자 / 요청하는게 아님
        
        # 데이터베이스 방문
        # 해당 글
        # 장고 ORM(pk: 무조건 pk로 작성한다.)
        post = Post.objects.get(pk=pk)
        # 댓글
        comments = Comment.objects.filter(post = post) 
        # 해시태그
        hashtags = HashTag.objects.filter(post = post)
        # 댓글 Form
        comment_form = CommentForm()
        # 태그 Form
        hashtag_form = HashTagForm()

        context = {
            'post' : post,
            'comments' : comments,
            'hashtags' : hashtags,
            'comment_form' : comment_form,
            'hashtag_form' : hashtag_form
        }

        return render(request, 'blog/post_detail.html', context)


### Comment
class CommentWrite(View):
    # def get(self, request):
    #     pass
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            # 사용자에게 댓글 내용을 받아옴
            content = form.cleaned_data['content']
            # 해당 아이디에 해당하는 글 불러옴
            post = Post.objects.get(pk=pk)
            # 댓글 객체 생성, create 메서드를 사용할 때는 save 필요없음
            comment = Comment.objects.create(post = post, content = content)
            # comment = Comment(post=post).
            return redirect('blog:detail', pk=pk)
        

class CommentDelete(View):
    def post(self, request, pk): # pk는 다른 말로 바꿔도 되는 것 위에 쓰인 pk와 다르다
        # 지울 객체를 찾아야 한다.-> 댓글 객체
        comment = Comment.objects.get(pk = pk)
        # 상세페이지로 들어가기
        post_id = comment.post.id 
        # 삭제
        comment.delete()

        return redirect('blog:detail', pk=post_id) 
    

### Tag
class HashTagWrite(View):
    def post(self, request, pk): # 여기서 pk는 post의 pk(id) 값
        form  = HashTagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            post = Post.objects.get(pk=pk)
            hashtag = HashTag.objects.create(post=post, name=name)
            return redirect('blog:detail', pk=pk)
        

class HashTagDelete(View):
    def post(self, request, pk): # 해시태그의 pk(id)값
        hashtag = HashTag.objects.get(pk=pk)
        post_id = hashtag.post.id
        hashtag.delete()
        return redirect('blog:detail', pk=post_id)
