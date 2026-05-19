"""
URL configuration for eventManagment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get_web/',views.login_get_web),
    path('admin_home/',views.admin_home),
    path('eventorgaiaser_home/',views.eventorgaiaser_home),
    path('student_home/',views.student_home),
    path('web_login/',views.web_login),
    path('Registering/',views.Registering),
    path('student_signupGet/',views.student_signupGet),
    path('studentSignup/',views.studentSignup),
    path('Organaizer_signupGet/',views.Organaizer_signupGet),
    path('Organaizer_signup/',views.Organaizer_signup),
    path('student_profile/',views.student_profile),
    path('organizer_profile/',views.organizer_profile),
    path('addEvent/',views.addEvent),
    path('addEventPost/',views.addEventPost),
    path('organaizerViewEvent/',views.organaizerViewEvent),
    path('deleteEvent/<id>',views.deleteEvent),
    path('eventViewEdit/<id>',views.eventViewEdit),
    path('eventEditPost/',views.eventEditPost),
    path('admin_view_events/',views.admin_view_events),
    path('approve_event/<id>',views.approve_event),
    path('Reject_event/<id>',views.reject_event),
    path('student_view_events/',views.student_view_events),
    path('book_event/<id>',views.book_event),
    path('student_booked_events/',views.student_booked_events),
    path('organizer_bookings/',views.organizer_bookings),
    path('admin_view_bookings/',views.admin_view_bookings),
    path('student_send_complaintGet/',views.student_send_complaintGet),
    path('student_send_complaint/',views.student_send_complaint),
    path('admin_view_complaints/',views.admin_view_complaints),
    path('adminSendReplayGet/<id>',views.adminSendReplayGet),
    path('adminSendReplay/',views.adminSendReplay),
    path('student_view_complaints/',views.student_view_complaints),
    path('admin_view_students/',views.admin_view_students),
    path('admin_view_organizers/',views.admin_view_organizers),
    path('student_edit_profile_get/',views.student_edit_profile_get),
    path('student_edit_profile/',views.student_edit_profile),
    path('organizer_edit_profile_get/',views.organizer_edit_profile_get),
    path('organizer_edit_profile/',views.organizer_edit_profile),
    path('adminChangePasswordGet/',views.adminChangePasswordGet),
    path('adminchangepasswordpost/',views.adminchangepasswordpost),
    path('OrganaizerChangePasswordGet/',views.OrganaizerChangePasswordGet),
    path('organaizerchangepasswordpost/',views.organaizerchangepasswordpost),
    path('StudentChangePasswordGet/',views.StudentChangePasswordGet),
    path('Studentchangepasswordpost/',views.Studentchangepasswordpost),
    path('logout_get/',views.logout_get),

    path('studentSendReviewGet/',views.studentSendReviewGet),
    path("student_add_review/<id>", views.studentSendReviewPost),
    path("admin_view_reviews/", views.admin_view_reviews),
    path('addRefree_get/',views.addRefree_get),
    path('adminViewRefree/',views.adminViewRefree),
    path('admin_addRefree/',views.admin_addRefree),
    path('refree_viewEdit/<id>',views.refree_viewEdit),
    path('editRefree/',views.editRefree),
    path('deleteRefree/<id>',views.deleteRefree),


    path('addShedule_get/<id>',views.addShedule_get),
    path('addShedulePost/',views.addShedulePost),
    path('viewShedule_get/',views.viewShedule_get),
    path('organaizerviewParticpents/<id>',views.organaizerviewParticpents),
    path('SetAsWinner/<id>',views.SetAsWinner),


    path('add_event_category_get/',views.add_event_category_get),
    path('add_event_category_post/',views.add_event_category_post),
    path('delete_event_category/<id>',views.delete_event_category),
    path('view_event_categories/',views.view_event_categories),
    path('event_add_poster/',views.event_add_poster),
    path('event_add_poster_post/',views.event_add_poster_post),
    path('event_view_posters/',views.event_view_posters),
    path('deleteposter/<id>',views.deleteposter),
    path('admin_viewWinners/<id>',views.admin_viewWinners),


]
