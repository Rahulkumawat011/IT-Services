import datetime
from random import randint
import pandas as pd
import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView, DetailView
from application.custom_classes import AjayDatatableView, AdminRequiredMixin, UserRequiredMixin

from .forms import CreateUserForm, EditUserForm, UserSignupForm, EditUserProfileForm
from .models import Subscription
from ..service.models import Service

User = get_user_model()


class CreateUserView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'admin/user/form.html'
    success_message = "User created successfully"
    success_url = reverse_lazy('admin-user-list')


class UpdateUserView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'admin/user/form.html'
    success_message = "User updated successfully"
    success_url = reverse_lazy('admin-user-list')


class ListUserView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/user/list.html'


class ListUserViewJson(AdminRequiredMixin, AjayDatatableView):
    model = User
    columns = ['first_name', 'last_name', 'email', 'is_active', 'actions']
    exclude_from_search_columns = ['actions']
    # extra_search_columns = ['']

    def get_initial_queryset(self):
        return self.model.objects.filter(Q(is_staff=False) | Q(is_superuser=False))

    def render_column(self, row, column):
        if column == 'is_active':
            if row.is_active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'

        if column == 'actions':
            detail_action = '<a href={} role="button" class="btn btn-info btn-xs mr-1 text-white">Detail</a>'.format(
                reverse('admin-user-detail', kwargs={'pk': row.pk}))
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('admin-user-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('admin-user-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListUserViewJson, self).render_column(row, column)


class DetailUserView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/user/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailUserView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=kwargs['pk'])
        return context


class DeleteUserView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


class ChangeUserPasswordView(AdminRequiredMixin, LoginRequiredMixin, View):
    form_class = SetPasswordForm
    template_name = 'admin/user/change_password.html'
    success_message = 'Password Updated Successfully!'

    def get(self, request, user_id, *args, **kwargs):
        form = self.form_class(get_object_or_404(User, pk=user_id))
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_id, *args, **kwargs):
        form = self.form_class(get_object_or_404(User, pk=user_id), request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('admin-user-list'))


class ListEmporiaView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/user/emporia_list.html'


@method_decorator(never_cache, name='dispatch')
class LandingView(View):
    admin_home_url = 'admin-dashboard'
    user_home_url = 'user-home'
    user_login_url = 'user-login'

    def get(self, request):
        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return HttpResponseRedirect(reverse(self.user_home_url))
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return HttpResponseRedirect(reverse(self.admin_home_url))
        return HttpResponseRedirect(reverse(self.user_login_url))


# Frontend user views

@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    template_name = 'user/user/login.html'
    success_url = 'user-home'
    login_url = 'user-login'
    success_message = 'You have successfully logged in.'
    failure_message = 'Please check credentials.'

    def get(self, request):
        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return HttpResponseRedirect(reverse(self.success_url))
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,
                            password=password)
        if user and not (user.is_superuser or user.is_staff):
            login(request, user)
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            messages.error(request, self.failure_message)
            return HttpResponseRedirect(reverse(self.login_url))


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user/user/register.html'
    success_message = "You have registered successfully"
    success_url = reverse_lazy('user-login')


class LogoutView(UserRequiredMixin, LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        return redirect('user-login')


class UpdateUserProfileView(UserRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditUserProfileForm
    template_name = 'user/user/profile.html'
    success_message = "Profile updated successfully"
    success_url = reverse_lazy('user-home')

    def get_object(self, queryset=None):
        return self.request.user


class ChangeUserSelfPasswordView(LoginRequiredMixin, View):
    template_name = 'user/user/change_password.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
        else:
            messages.error(request, 'Error occurred while changing password, please enter a proper password.')
            return render(request, self.template_name, {'form': form})
        return redirect('user-profile')


class HomePageView(TemplateView):
    template_name = 'user/user/home.html'

    def get_context_data(self, **kwargs):
        kwargs = super(HomePageView, self).get_context_data(**kwargs)
        return kwargs


class ListServiceUserViewJson(AjayDatatableView):
    model = Service
    columns = ["service_name", "payment_terms", "service_price", "service_package", "service_tax", "service_image",  "Active", 'actions']
    exclude_from_search_columns = ['actions']

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        if column == 'active':
            if row.active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'

        if column == 'actions':
            buynow_action = '<a href={} role="button" class="btn btn-success btn-xs mr-1 text-white">Buy Service</a>'.format(
                reverse('buy-service', kwargs={'pk': row.pk}))
            # edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
            #     reverse('service-edit', kwargs={'pk': row.pk}))
            # buynow_action = '<a href="javascript:;" class="remove_record btn btn-success btn-xs" data-url={} role="button">Buy Now</a>'.format(
            #     reverse('service-delete', kwargs={'pk': row.pk}))
            return buynow_action
        else:
            return super(ListServiceUserViewJson, self).render_column(row, column)


class BuyServiceView(DetailView):
    model = Service
    template_name = 'user/user/buy.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_image'] = context['service_image'] = self.model.objects.all()
        return context


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

def subscribe_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    amount = service.total_price * 100  # Multiply by 100 to convert to the smallest currency unit


    # Create Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=int(amount), currency='INR', payment_capture='0'))
    razorpay_order_id = razorpay_order['id']

    # Create Subscription record
    subscription = Subscription.objects.create(
        user=request.user,
        service=service,
        amount=service.total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status='Pending'
    )

    context = {
        'service': service,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': int(amount),  # Ensure the amount is an integer
        'currency': 'INR',
        'callback_url': request.build_absolute_uri('/razorpay/callback/'),
    }

    return render(request, 'user/user/subscription.html', context)


# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def razorpay_callback(request):
    print('Enter the functions')
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        print(payment_id,'Empty Value')
        print(razorpay_order_id, 'Empty Value')
        print(razorpay_signature, 'Empty Value')
        # Fetch the subscription details
        subscription = Subscription.objects.get(razorpay_order_id=razorpay_order_id)

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            subscription.payment_id = payment_id
            subscription.payment_status = 'Success'
            subscription.razorpay_payment_id = payment_id
            subscription.razorpay_signature = razorpay_signature
            print("Payment Successfully")
            subscription.save()
            print("error found")
            # Redirect to a success page or handle the successful payment as needed
            return redirect('subscription_success')
        except razorpay.errors.SignatureVerificationError:
            subscription.payment_status = 'Failed'
            subscription.save()
            # Redirect to a failure page or handle the failed payment as needed
            return redirect('payment-failure')

    return redirect('user-home')

def subscription_success(request):
    return render(request,'user/user/success.html')