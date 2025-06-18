from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max, Count
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .models import Item, Category, User, ItemImage, Message
from .forms import ItemForm
import json

User = get_user_model()

def home(request):
    recent_items = Item.objects.filter(
        is_approved=True, 
        item_status='active'
    ).select_related('category', 'posted_by')[:6]
    
    context = {
        'recent_items': recent_items,
    }
    return render(request, 'index.html', context)



@login_required
def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for image in images:
                ItemImage.objects.create(item=item, image=image)
            
            messages.success(request, 'Item posted successfully!')
            return redirect('lost_found:item_detail', pk=item.pk)
       
    else:
        form = ItemForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        
    }
    return render(request, 'post-item.html', context)



@login_required
def my_items(request):
    items = Item.objects.filter(posted_by=request.user).select_related(
        'category').order_by('-created_at')
    
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'my-items.html', context)

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
           
            # Handle new image uploads
            images = request.FILES.getlist('images')
            for image in images:
                ItemImage.objects.create(item=item, image=image)
            
            messages.success(request, 'Item updated successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'categories': Category.objects.all(),
        
    }
    return render(request, 'edit-item.html', context)

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('lost_found:my_items')



def search_items(request):
    items = Item.objects.filter(
        is_approved=True, 
        item_status='active'
    ).select_related('category', 'posted_by')
    
    # Search query
    query = request.GET.get('search', '')
    if query:
        items = items.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Filter by status
    status = request.GET.get('status', '')
    if status and status != 'all':
        items = items.filter(status=status)
    
    # Filter by category
    category = request.GET.get('category', '')
    if category:
        items = items.filter(category__slug=category)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        items = items.filter(location__in=location)
    
    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        items = items.filter(date_lost_found__gte=date_from)
    if date_to:
        items = items.filter(date_lost_found__lte=date_to)
    
    # Sort
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        items = items.order_by('created_at')
    elif sort_by == 'az':
        items = items.order_by('title')
    elif sort_by == 'za':
        items = items.order_by('-title')
    else:  # newest
        items = items.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'current_filters': {
            'search': query,
            'status': status,
            'query_string': query_params.urlencode(),
            'category': category,
            'location': location,
            'date_from': date_from,
            'date_to': date_to,
            'sort': sort_by,
        }
    }
    return render(request, 'search.html', context)

def item_detail(request, pk):
    item = get_object_or_404(
        Item.objects.select_related('category', 'posted_by'),
        pk=pk,
        is_approved=True
    )
    
    # Get item images
    images = item.images.all()
    
    # Get messages for this item (if user is the owner)
    messages_list = []
    if request.user.is_authenticated and request.user == item.posted_by:
        messages_list = item.messages.select_related('sender').order_by('-created_at')
    
    context = {
        'item': item,
        'images': images,
        'messages': messages_list,
    }
    return render(request, 'item-detail.html', context)


@login_required
def mark_item_resolved(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    item.item_status = 'resolved'
    item.status = 'found'
    item.save()
    
    messages.success(request, 'Item marked as resolved!')
    return redirect('lost_found:item_detail', pk=item.pk)


@login_required
def mark_item_active(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    item.item_status = 'active'
    item.save()
    
    messages.success(request, 'Item marked as active!')
    return redirect('lost_found:item_detail', pk=item.pk)



@login_required
def send_message(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.posted_by == request.user:
        # Optional: Prevent sending messages to yourself
        return redirect(item.get_absolute_url())

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                item=item,
                sender=request.user,
                receiver=item.posted_by,
                content=content
            )
            
            messages.success(request, "Message sent successfully.")
            return redirect(item.get_absolute_url())

    return render(request, 'send_message.html', {'item': item})


@login_required
def inbox(request):
    
    grouped_threads = (
        Message.objects
        .filter(Q(receiver=request.user) | Q(sender=request.user))
        .values('sender_id', 'sender__username', 'item_id', 'item__title')
        .annotate(latest=Max('created_at'),
                  
                  unread_count=Count('id', filter=Q(receiver=request.user, is_read=False))
                  )
        .order_by('-latest')
    )
    return render(request, 'inbox.html', {'inbox': grouped_threads})


@login_required
def read_inbox(request, item_id, sender_id):
    messages = Message.objects.filter(
        Q(sender_id=sender_id,  item_id=item_id) | Q(receiver_id=sender_id, item_id=item_id)
    ).order_by('created_at')

    item = get_object_or_404(Item, pk=item_id)
    sender = get_object_or_404(User, pk=sender_id)
    
    Message.objects.filter(
        Q(sender_id=sender_id,  item_id=item_id) | Q(receiver_id=sender_id, item_id=item_id)
    ).update(is_read = True)
    
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                item=item,
                sender=request.user,
                receiver=sender,
                content=content
            )
            return redirect('lost_found:read_inbox', item_id=item_id, sender_id=sender_id)

    return render(request, 'inbox_detail.html', {'inbox_messages': messages, 'item': item, 'sender': sender})