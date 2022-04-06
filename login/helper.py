from circle.models import CirclePolicyCompliance


def update_compliance(username, circle_id, policy_id, compliance):
    try:
        policy_compliance = CirclePolicyCompliance.objects.get(
            username=username, circle_id=circle_id, policy_id=policy_id
        )

        policy_compliance.compliance = compliance

        policy_compliance.save()
    except Exception:
        pass
