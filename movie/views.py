
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse,HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .forms import UserForm, ProfileForm
from .models import Movie, FavoriteMovie, Category, review, Profile
from django.contrib.auth.models import User
from django.contrib import messages

User = get_user_model()


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                        password=password)
        user.save()
        messages.success(request, 'Registration successful. Welcome!')
        return redirect('login')

    return render(request, 'reg.html')


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['email'] = user.email  # Store user email in session
            messages.success(request, 'Login successful. Welcome back!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')


@login_required
def home_view(request):
    movies_list = Movie.objects.all().order_by('title')  # Order movies by title
    paginator = Paginator(movies_list, 9)  # Show 9 movies per page

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'movies': movies})


@login_required
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        release_date = request.POST.get('release_date', '')
        actors = request.POST.get('actors', '')
        category = request.POST.get('category', '')
        trailer_link = request.POST.get('trailer_link', '')
        image = request.FILES.get('image', None)

        movie = Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            actors=actors,
            category=category,
            trailer_link=trailer_link,
            image=image,
            user=request.user

        )

        return redirect('home')

    return render(request, 'index.html')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})


def note_view(request):
    return render(request, 'note.html')


@login_required
def get_movie_details(request):
    movie_id = request.GET.get('movieId')
    if movie_id:
        try:
            movie = Movie.objects.get(pk=movie_id)
            movie_data = {
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'release_date': movie.release_date,
                'actors': movie.actors,
                'category': movie.category,
                'trailer_link': movie.trailer_link,
                'image': movie.image.url,
            }
            return JsonResponse(movie_data)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)
    else:
        return JsonResponse({'error': 'Missing movieId parameter'}, status=400)


def note(request, ):
    return render(request, 'note.html')


def search(request):
    query = request.GET.get('q')
    error_message = None

    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(actors__icontains=query))
        if not movies.exists():
            error_message = "No movies found matching your search criteria."
    else:
        movies = Movie.objects.all()

    paginator = Paginator(movies, 9)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    return render(request, 'search.html', {'movies': movies, 'error_message': error_message})



@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get_or_create(user=user)[0]

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
    })
@require_http_methods(["GET", "POST"])
@login_required
def review_page(request, id):
    try:
        item_details = get_object_or_404(Movie, id=id)
    except ValueError:
        return render(request, 'error_page.html', {'error_message': 'Invalid Movie ID'})

    if request.method == 'POST':
        review_desp = request.POST.get('review_desp')
        rating = request.POST.get('rating')

        new_review = review(user=request.user, item=item_details, review_desp=review_desp, rating=rating)
        new_review.save()

        messages.success(request, 'Review added successfully.')
        return redirect('review_page', id=id)  # Redirect to the same page to see the new review

    reviews = review.objects.filter(item=item_details)

    return render(request, 'review_page.html', {'item_details': item_details, 'reviews': reviews})


@login_required
def favorite(request):
    movie_id = request.GET.get('movieId')
    movie = get_object_or_404(Movie, pk=movie_id)

    favorite, created = FavoriteMovie.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        # If the favorite already exists, it means the user wants to unfavorite it
        favorite.delete()
        message = 'The movie has been removed from your favorite list.'
    else:
        message = 'The movie has been added to your favorite list.'

    # Redirect back to the movie list page with a message
    return redirect('favorite_list')


@login_required
def favorite_list(request):
    favorite_movies_list = FavoriteMovie.objects.filter(user=request.user).select_related('movie')
    paginator = Paginator(favorite_movies_list, 9)  # Show 9 favorite movies per page

    page = request.GET.get('page')
    try:
        favorite_movies = paginator.page(page)
    except PageNotAnInteger:
        favorite_movies = paginator.page(1)
    except EmptyPage:
        favorite_movies = paginator.page(paginator.num_pages)

    return render(request, 'favorite.html', {'favorite_movies': favorite_movies})


@login_required
def delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this movie.")
    if request.method == 'POST':
        movie.delete()
        return redirect('home')
    return render(request, 'delete.html', {'movie': movie})




@login_required
def edit(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Ensure that the user editing the movie is the one who added it
    if movie.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this movie.")

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        release_date = request.POST.get('release_date', '').strip()
        actors = request.POST.get('actors', '').strip()
        category = request.POST.get('category', '').strip()
        trailer_link = request.POST.get('trailer_link', '').strip()
        image = request.FILES.get('image')

        # Check if all fields are filled
        if title and description and release_date and actors and category and trailer_link:
            movie.title = title
            movie.description = description
            movie.release_date = release_date
            movie.actors = actors
            movie.category = category
            movie.trailer_link = trailer_link
            if image:
                movie.image = image
            movie.save()
            return redirect('home')
        else:
            messages.error(request, 'Please fill in all information details.')

    return render(request, 'edit.html', {'movie': movie})