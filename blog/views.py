from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Post, Vote
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'MEDIA_URL': settings.MEDIA_URL})

def features_view(request):
    return render(request, 'blog/features.html')

# FAQs page view
def faqs_view(request):
    return render(request, 'blog/faqs.html')

def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        # Check if the user has already voted
        if Vote.objects.filter(user=request.user, post=post, vote_type='upvote').exists():
            return JsonResponse({'success': False, 'message': 'You have already upvoted this post.'})

        # Check if the user has already downvoted
        if Vote.objects.filter(user=request.user, post=post, vote_type='downvote').exists():
            return JsonResponse({'success': False, 'message': 'You cannot upvote after downvoting.'})

        # Process the upvote logic
        post.total_upvotes += 1
        post.save()

        # Record the vote
        Vote.objects.create(user=request.user, post=post, vote_type='upvote')

        return JsonResponse({'success': True, 'total_upvotes': post.total_upvotes})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def downvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # Check if the user has already voted
        if Vote.objects.filter(user=request.user, post=post, vote_type='downvote').exists():
            return JsonResponse({'success': False, 'message': 'You have already downvoted this post.'})

        # Check if the user has already upvoted
        if Vote.objects.filter(user=request.user, post=post, vote_type='upvote').exists():
            return JsonResponse({'success': False, 'message': 'You cannot downvote after upvoting.'})

        # Process the downvote logic
        post.total_downvotes += 1
        post.save()

        # Record the vote
        Vote.objects.create(user=request.user, post=post, vote_type='downvote')

        return JsonResponse({'success': True, 'total_downvotes': post.total_downvotes})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-date_posted')
        context['comment_form'] = CommentForm()

        # Check if the user has already upvoted or downvoted the post
        context['user_has_upvoted'] = Vote.objects.filter(user=self.request.user, post=self.object, vote_type='upvote').exists()
        context['user_has_downvoted'] = Vote.objects.filter(user=self.request.user, post=self.object, vote_type='downvote').exists()

        total_likes = self.object.total_upvotes - self.object.total_downvotes
        context['total_likes'] = total_likes  
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            if request.is_ajax():
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'user': comment.user.username,
                        'date_posted': comment.date_posted.strftime('%Y-%m-%d %H:%M:%S'),
                        'content': comment.content
                    }
                })
            return redirect('blog-detail', pk=post.pk)
        else:
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors})
            return self.get(request, *args, **kwargs)
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False