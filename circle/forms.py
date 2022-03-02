# from django import forms
# from .models import Policy


# class RequestCircle(forms.Form):
#     circle_id = forms.CharField(label='Circle ID', max_length=50)


# class CircleCreate(forms.Form):

#     def create_choices(Policy):
#         policy_name = list()
#         policy_id = list()

#         for query in Policy.objects.all():
#             policy_name.append(query.policy_name)
#             policy_id.append(query.policy_id)

#         choices = [(policy_id[i], policy_name[i])
#                    for i in range(0, len(policy_name))]
#         return tuple(choices)

#     circle_name = forms.CharField(label='Circle Name', max_length=50)
#     policy = forms.ChoiceField(
#         choices=create_choices(Policy), label='Circle Policy'
#     )
